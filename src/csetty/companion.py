# ruff: noqa: E501
from __future__ import annotations

import argparse
import html
import json
import os
import secrets
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

from .course_resources import CourseResourceLink, course_resource_links
from .docker_runtime import DockerRuntime
from .errors import CSETTYError, StateError, ToolUnavailableError, ValidationError
from .models import Attempt, AttemptState
from .pack import Pack, load_pack
from .paths import AppPaths
from .storage import Store, process_is_alive
from .supervisor import ensure_supervisor
from .util import atomic_write
from .vscode import VSCodeManager
from .web_render import markdown_to_html
from .web_theme import course_navbar, course_theme_class, theme_style

_MAX_REQUEST_BYTES = 4096
_START_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True)
class CompanionInfo:
    attempt_id: str
    pid: int
    port: int
    token: str
    started_at: str

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}/{self.token}"

    @property
    def url(self) -> str:
        return f"{self.base_url}/"


def _attempt_root(paths: AppPaths, attempt_id: str) -> Path:
    return paths.attempts / attempt_id


def _manifest_path(paths: AppPaths, attempt_id: str) -> Path:
    return _attempt_root(paths, attempt_id) / "companion.json"


def _read_info(paths: AppPaths, attempt_id: str) -> CompanionInfo | None:
    manifest = _manifest_path(paths, attempt_id)
    try:
        raw = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    try:
        info = CompanionInfo(
            attempt_id=str(raw["attempt_id"]),
            pid=int(raw["pid"]),
            port=int(raw["port"]),
            token=str(raw["token"]),
            started_at=str(raw["started_at"]),
        )
    except (KeyError, TypeError, ValueError):
        return None
    if (
        info.attempt_id != attempt_id
        or info.pid <= 0
        or not 1 <= info.port <= 65535
        or len(info.token) < 32
    ):
        return None
    return info


def _healthy(info: CompanionInfo) -> bool:
    if not process_is_alive(info.pid):
        return False
    request = urllib.request.Request(
        f"{info.base_url}/health",
        headers={"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=0.5) as response:
            return int(response.status) == HTTPStatus.OK
    except (OSError, urllib.error.URLError):
        return False


def launch_companion(
    paths: AppPaths,
    attempt: Attempt,
    *,
    open_browser: bool = True,
    browser_open: Callable[[str], object] = webbrowser.open,
    ready_callback: Callable[[], None] | None = None,
) -> CompanionInfo:
    """Start or reuse the loopback-only page for an attempt."""

    def publish(info: CompanionInfo) -> CompanionInfo:
        if open_browser:
            try:
                opened = browser_open(info.url)
            except Exception as exc:
                if ready_callback is not None:
                    raise ToolUnavailableError(
                        "exam paper is ready, but the browser failed to open; "
                        f"reading time has not started: {info.url}"
                    ) from exc
                opened = False
            if opened is False and ready_callback is not None:
                raise ToolUnavailableError(
                    "exam paper is ready, but the browser could not be opened "
                    f"automatically; reading time has not started: {info.url}"
                )
        if ready_callback is not None:
            ready_callback()
        return info

    existing = _read_info(paths, attempt.id)
    if existing is not None and _healthy(existing):
        return publish(existing)

    root = _attempt_root(paths, attempt.id)
    root.mkdir(parents=True, exist_ok=True)
    lock = root / "companion.starting"
    owns_lock = False
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(descriptor)
        owns_lock = True
    except FileExistsError:
        pass

    process: subprocess.Popen[bytes] | None = None
    try:
        if owns_lock:
            log_path = root / "companion.log"
            with log_path.open("ab", buffering=0) as log:
                kwargs: dict[str, Any] = {
                    "stdin": subprocess.DEVNULL,
                    "stdout": log,
                    "stderr": log,
                    "close_fds": True,
                }
                if os.name == "nt":
                    detached = getattr(subprocess, "DETACHED_PROCESS", 0)
                    new_group = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
                    kwargs["creationflags"] = detached | new_group
                else:
                    kwargs["start_new_session"] = True
                try:
                    process = subprocess.Popen(
                        [
                            sys.executable,
                            "-m",
                            "csetty.companion",
                            "--serve",
                            "--state-dir",
                            str(paths.root),
                            "--attempt",
                            attempt.id,
                        ],
                        **kwargs,
                    )
                except OSError as exc:
                    raise ToolUnavailableError(
                        f"exam companion page failed to start: {exc}"
                    ) from exc

        deadline = time.monotonic() + _START_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            info = _read_info(paths, attempt.id)
            if info is not None and _healthy(info):
                return publish(info)
            if process is not None and process.poll() is not None:
                detail = (root / "companion.log").read_text(
                    encoding="utf-8", errors="replace"
                ).strip()
                suffix = f": {detail}" if detail else ""
                raise ToolUnavailableError(f"exam companion page failed to start{suffix}")
            time.sleep(0.05)
    finally:
        if owns_lock:
            lock.unlink(missing_ok=True)
    if process is not None and process.poll() is None:
        try:
            process.kill()
            process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            pass
    raise ToolUnavailableError(
        f"exam companion page did not start; inspect {root / 'companion.log'}"
    )


class CompanionApplication:
    def __init__(
        self,
        *,
        paths: AppPaths,
        store: Store,
        runtime: DockerRuntime,
        vscode: VSCodeManager,
        attempt_id: str,
        token: str,
        reopen_callback: Callable[[], str] | None = None,
    ) -> None:
        self.paths = paths
        self.store = store
        self.runtime = runtime
        self.vscode = vscode
        self.attempt_id = attempt_id
        self.token = token
        self._reopen_callback = reopen_callback
        self._reopen_lock = threading.Lock()
        self._last_reopen = 0.0

    @property
    def base_path(self) -> str:
        return f"/{self.token}"

    def attempt_and_pack(self) -> tuple[Attempt, Pack]:
        attempt = self.store.get_attempt(self.attempt_id)
        pack = load_pack(attempt.pack_path)
        if pack.digest != attempt.pack_digest:
            raise ValidationError("attempt pack content changed after attempt creation")
        return attempt, pack

    @staticmethod
    def _countdown_end(attempt: Attempt, pack: Pack) -> datetime | None:
        if attempt.state is AttemptState.READING and attempt.reading_started_at is not None:
            return attempt.reading_started_at + timedelta(seconds=pack.reading_time_seconds)
        return attempt.deadline_at

    @classmethod
    def _remaining_seconds(cls, attempt: Attempt, pack: Pack) -> int | None:
        countdown_end = cls._countdown_end(attempt, pack)
        if countdown_end is None:
            return None
        return max(0, int((countdown_end - datetime.now(UTC)).total_seconds()))

    @staticmethod
    def _remaining_text(seconds: int | None) -> str:
        if seconds is None:
            return "Untimed"
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def status_document(self) -> dict[str, Any]:
        attempt, pack = self.attempt_and_pack()
        latest: dict[str, Mapping[str, Any]] = {}
        for submission in self.store.list_submissions(attempt.id):
            latest[submission["question_id"]] = submission
        return {
            "attempt_id": attempt.id,
            "course": pack.course,
            "state": attempt.state.value,
            "remaining_seconds": self._remaining_seconds(attempt, pack),
            "deadline_at": (
                None if attempt.deadline_at is None else attempt.deadline_at.isoformat()
            ),
            "report_ready": self.report_ready(attempt),
            "questions": [
                {
                    "id": question.id,
                    "submitted": question.id in latest,
                    "sequence": (
                        None
                        if question.id not in latest
                        else int(latest[question.id]["sequence"])
                    ),
                }
                for question in pack.questions
            ],
        }

    def report_ready(self, attempt: Attempt | None = None) -> bool:
        current = attempt or self.store.get_attempt(self.attempt_id)
        report = self.paths.reports / f"{self.attempt_id}.html"
        json_report = self.paths.reports / f"{self.attempt_id}.json"
        grade = self.store.get_grade(self.attempt_id)
        return (
            current.state.terminal
            and grade is not None
            and grade.get("report_finalized_at") is not None
            and json_report.is_file()
            and not json_report.is_symlink()
            and report.is_file()
            and not report.is_symlink()
        )

    def render_report(self) -> str:
        attempt = self.store.get_attempt(self.attempt_id)
        if not self.report_ready(attempt):
            raise StateError("the final report is not ready yet")
        return (self.paths.reports / f"{self.attempt_id}.html").read_text(encoding="utf-8")

    def reopen_code(self) -> str:
        with self._reopen_lock:
            attempt, pack = self.attempt_and_pack()
            if attempt.state is not AttemptState.WORKING:
                raise StateError(f"VS Code is unavailable while attempt is {attempt.state.value}")
            if attempt.editor != "code":
                raise StateError(
                    "this attempt was started with --editor terminal; reopen its terminal with csetty resume"
                )
            now = time.monotonic()
            if now - self._last_reopen < 2.0:
                raise StateError("VS Code reopen was requested too recently; wait two seconds")
            self._last_reopen = now
            if self._reopen_callback is not None:
                return self._reopen_callback()
            ready, detail = self.vscode.offline_ready(attempt.profile)
            if not ready:
                raise ToolUnavailableError(detail)
            self.runtime.start_container(attempt, pack, network=attempt.network)
            ensure_supervisor(self.paths, attempt)
            self.vscode.attach(attempt)
            return "A request to reopen the isolated VS Code window was sent successfully."

    def _navigation(self, pack: Pack, active: str | None = None) -> str:
        question_items = []
        for index, question in enumerate(pack.questions, start=1):
            selected = ' aria-current="page"' if question.id == active else ""
            question_items.append(
                f'<a{selected} href="{self.base_path}/#question-{html.escape(question.id, quote=True)}">'
                f"Q{index}. {html.escape(question.title)}</a>"
            )
        return (
            f'<a href="{self.base_path}/">Paper</a>'
            '<details class="nav-menu">'
            '<summary>Questions</summary>'
            f'<div class="nav-menu-items">{"".join(question_items)}</div>'
            "</details>"
        )

    @staticmethod
    def _require_paper_available(attempt: Attempt) -> None:
        if attempt.state is AttemptState.CREATED:
            raise StateError(
                "reading time has not started; the exam paper is not available yet"
            )

    def _layout(
        self,
        *,
        attempt: Attempt,
        pack: Pack,
        title: str,
        content: str,
        active: str | None = None,
        message: str | None = None,
        error: bool = False,
    ) -> str:
        remaining = self._remaining_seconds(attempt, pack)
        timer = self._remaining_text(remaining)
        message_html = ""
        if message:
            message_html = (
                f'<div class="message alert {"alert-danger" if error else "alert-success"}">'
                f"{html.escape(message)}</div>"
            )
        countdown_end = self._countdown_end(attempt, pack)
        deadline = "" if countdown_end is None else countdown_end.isoformat()
        created = attempt.state is AttemptState.CREATED
        reading = attempt.state is AttemptState.READING
        if created:
            timer = "Waiting"
            timer_label = "Reading not started"
            surface_label = "Local CSEExamTTY exam launch"
        elif reading:
            timer_label = "Reading time remaining"
            surface_label = "Local CSEExamTTY read-only exam paper"
        else:
            timer_label = "Remaining"
            surface_label = "Local CSEExamTTY practice examination"
        status_url = f"{self.base_path}/status.json"
        report_url = f"{self.base_path}/report"
        theme_class = course_theme_class(pack.profile, pack.course)
        total_marks = sum(question.points for question in pack.questions)
        navbar = course_navbar(
            course=pack.course,
            home_url=f"{self.base_path}/",
            links="" if created else self._navigation(pack, active),
            status=(
                f'<span class="phase-badge">{html.escape(attempt.state.value)}</span>'
                f'<span>{timer_label}: <span class="timer" data-countdown>{timer}</span></span>'
            ),
        )
        hero_summary = (
            '<p class="lead">The paper remains hidden until reading time starts.</p>'
            if created
            else (
                f'<p class="lead">{len(pack.questions)} questions — {total_marks} marks<br>'
                f'{html.escape(timer_label)}: <span data-countdown>{timer}</span></p>'
            )
        )
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="same-origin">
<title>{html.escape(title)} — {html.escape(pack.course)} — CSEExamTTY</title>
{theme_style()}
<style>
.timer {{ font:700 1rem SFMono-Regular,Menlo,Monaco,Consolas,monospace; }}
.phase-badge {{ padding:.15rem .4rem; color:#212529; font-size:.75rem; font-weight:700; background:#fff; border-radius:.2rem; }}
.question-prompt > h1:first-child {{ display:none; }}
.question-meta {{ margin:.5rem 0 1rem; }}
.paper-question {{ scroll-margin-top:5rem; }}
.paper-question .section-heading small {{ color:var(--muted); font-size:60%; font-weight:400; }}
.message {{ margin-bottom:1rem; }}
@media (max-width:760px) {{ .navbar-status {{ font-size:.78rem; }} }}
</style>
</head>
<body class="{theme_class}" data-deadline="{html.escape(deadline, quote=True)}" data-state="{html.escape(attempt.state.value, quote=True)}" data-status-url="{html.escape(status_url, quote=True)}" data-report-url="{html.escape(report_url, quote=True)}">
{navbar}
<main class="container" aria-label="Content">
<header class="exam-hero">
<p class="text-muted text-uppercase"><strong>{surface_label}</strong></p>
<h1>{html.escape(pack.title)}</h1>
{hero_summary}
<p class="text-muted">Candidate {html.escape(attempt.candidate_id or 'practice user')} · not made or managed by UNSW</p>
</header>
{message_html}{content}
</main>
<script>
(() => {{
  const deadline = document.body.dataset.deadline;
  const initialState = document.body.dataset.state;
  const statusUrl = document.body.dataset.statusUrl;
  const reportUrl = document.body.dataset.reportUrl;
  const timers = document.querySelectorAll('[data-countdown]');
  const update = () => {{
    if (!deadline || timers.length === 0) return;
    const seconds = Math.max(0, Math.floor((Date.parse(deadline) - Date.now()) / 1000));
    const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const s = String(seconds % 60).padStart(2, '0');
    const text = `${{h}}:${{m}}:${{s}}`;
    timers.forEach((timer) => {{ timer.textContent = text; }});
  }};
  update(); setInterval(update, 1000);
  const refreshOnStateChange = async () => {{
    if (!initialState || !statusUrl) return;
    try {{
      const response = await fetch(statusUrl, {{ cache: 'no-store' }});
      if (!response.ok) return;
      const status = await response.json();
      if (status.report_ready && reportUrl) {{
        window.location.assign(reportUrl);
        return;
      }}
      if (status.state !== initialState) window.location.reload();
    }} catch (_error) {{
      // A transient local-page failure is retried on the next poll.
    }}
  }};
  const pollLoop = async () => {{
    await refreshOnStateChange();
    setTimeout(pollLoop, 1000);
  }};
  pollLoop();
}})();
</script>
</body>
</html>"""

    def _resource_sections(self, pack: Pack, *, include_external: bool = True) -> str:
        sections: dict[str, list[CourseResourceLink]] = {}
        if include_external:
            for link in course_resource_links(pack.profile):
                sections.setdefault(link.section, []).append(link)
        external = []
        for section, links in sections.items():
            items = "".join(
                f'<li><a href="{html.escape(link.url, quote=True)}" target="_blank" '
                f'rel="noopener noreferrer">{html.escape(link.label)}</a></li>'
                for link in links
            )
            external.append(
                f'<section class="resource-section"><h3>{html.escape(section)}</h3>'
                f"<ul>{items}</ul></section>"
            )
        local = ""
        if pack.resources:
            items = "".join(
                f'<li><a href="{self.base_path}/resource/{index}">{html.escape(resource.label)}</a></li>'
                for index, resource in enumerate(pack.resources)
            )
            local = f'<section class="resource-section"><h3>Bundled local resources</h3><ul>{items}</ul></section>'
        return local + "".join(external)

    def render_overview(self, *, message: str | None = None, error: bool = False) -> str:
        attempt, pack = self.attempt_and_pack()
        if attempt.state is AttemptState.CREATED:
            content = """
<section class="exam-section">
<header class="section-heading"><h2>Waiting to start reading time</h2></header>
<div class="alert alert-course">
<p>The browser page is ready, but the paper remains hidden and the reading clock has not started.</p>
<p>Return to the terminal and run <code>csetty resume</code> to retry the browser launch and begin reading.</p>
</div>
</section>"""
            return self._layout(
                attempt=attempt,
                pack=pack,
                title="Exam launch",
                content=content,
                message=message,
                error=error,
            )
        latest = {
            submission["question_id"]: submission
            for submission in self.store.list_submissions(attempt.id)
        }
        rows = []
        question_sections = []
        for index, question in enumerate(pack.questions, start=1):
            submission = latest.get(question.id)
            if attempt.state is AttemptState.READING:
                status = "Locked during reading time"
                status_class = "alert-course"
            else:
                status = (
                    "Not submitted"
                    if submission is None
                    else f"Submitted #{submission['sequence']}"
                )
                status_class = "alert-warning" if submission is None else "alert-success"
            tags = "".join(f'<span class="badge">{html.escape(tag)}</span>' for tag in question.tags)
            files = ", ".join(
                f"<code>{html.escape(path)}</code>" for path in question.submission_files
            )
            rows.append(
                "<tr>"
                f'<td><a href="#question-{html.escape(question.id, quote=True)}">Q{index}</a></td>'
                f"<td>{html.escape(question.title)}<br>{tags}</td>"
                f"<td>{question.points}</td><td>{html.escape(question.track)}</td>"
                f"<td>{html.escape(status)}</td></tr>"
            )
            question_sections.append(
                f'<section class="exam-section paper-question" id="question-{html.escape(question.id, quote=True)}">'
                '<header class="section-heading">'
                f"<h2>Question {index} <small>({question.points} marks)</small></h2>"
                f"<p>{html.escape(question.title)}</p></header>"
                f'<p class="question-meta">{tags}</p>'
                f'<div class="alert {status_class}"><strong>Submission:</strong> {files} · '
                f"<strong>Status:</strong> {html.escape(status)}</div>"
                f'<article class="question-prompt">{markdown_to_html(pack.question_prompt(question))}</article>'
                '<div class="actions no-print">'
                f'<a class="btn" href="{self.base_path}/question/{html.escape(question.id, quote=True)}">'
                "Open focused question view</a></div></section>"
            )
        if attempt.state is AttemptState.READING:
            editor_control = ""
            editor_text = (
                "Reading time is read-only. Read every complete question using the "
                "navigation; the workspace and editor remain locked until working time begins."
            )
            controls_heading = "Reading time"
            controls_text = editor_text
        elif attempt.editor == "code" and attempt.state is AttemptState.WORKING:
            editor_control = (
                f'<form method="post" action="{self.base_path}/reopen-code">'
                '<button class="btn" type="submit">Open VSC</button></form>'
            )
            editor_text = (
                "Use this recovery control to reconnect to the existing supervised Docker "
                "container; it does not create a new attempt."
            )
            controls_heading = "Exam controls"
            controls_text = f"Closing the editor does not stop the clock. {editor_text}"
        elif attempt.editor == "code":
            editor_control = ""
            editor_text = (
                f"VS Code recovery is unavailable because this attempt is "
                f"{attempt.state.value}."
            )
            controls_heading = "Exam controls"
            controls_text = f"Closing the editor does not stop the clock. {editor_text}"
        else:
            editor_control = ""
            editor_text = "This attempt uses terminal mode. Run csetty resume to reopen its terminal."
            controls_heading = "Exam controls"
            controls_text = f"Closing the editor does not stop the clock. {editor_text}"
        if attempt.state.terminal:
            if self.report_ready(attempt):
                editor_control = (
                    f'<a class="btn" href="{self.base_path}/report">Open final report</a>'
                )
                controls_text += " The final report is ready."
            else:
                editor_control = (
                    '<span class="btn" aria-disabled="true">Preparing final report…</span>'
                )
                controls_text += " The final report will open automatically when ready."
        if attempt.state is AttemptState.READING:
            resources_text = (
                "Only the bundled resources explicitly permitted by this paper are available "
                "during reading time."
            )
            resources = self._resource_sections(pack, include_external=False)
            resources_heading = "Permitted resources"
        else:
            resources_text = (
                "Bundled resources are available offline. Official public links are an index "
                "only: their content is not copied into CSEExamTTY and requires host network "
                "access. Docker remains subject to the attempt network policy."
            )
            resources = self._resource_sections(pack)
            resources_heading = "Course resources"
        content = f"""
<section class="exam-section" id="instructions">
<header class="section-heading"><h2>Examination information</h2></header>
<div class="alert alert-warning">
<h3>Local simulation notice</h3>
<p>This original mock exam system is not made or managed by the UNSW School of Computer Science and Engineering. Submissions remain on this computer and are not sent to UNSW.</p>
</div>
<div class="alert alert-course">
<h3>{controls_heading}</h3>
<p>{controls_text}</p>
<div class="actions">{editor_control}</div>
</div>
</section>
<section class="exam-section" id="paper-at-a-glance">
<header class="section-heading"><h2>Paper at a glance</h2></header>
<div class="table-scroll"><table><thead><tr><th>#</th><th>Question</th><th>Marks</th><th>Track</th><th>Submission</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</section>
<h1 id="questions">Questions</h1>
{''.join(question_sections)}
<section class="exam-section" id="resources">
<header class="section-heading"><h2>{resources_heading}</h2></header>
<p class="muted">{resources_text}</p>
<div class="resource-grid">{resources}</div>
</section>"""
        return self._layout(
            attempt=attempt,
            pack=pack,
            title="Exam overview",
            content=content,
            message=message,
            error=error,
        )

    def render_question(self, question_id: str) -> str:
        attempt, pack = self.attempt_and_pack()
        self._require_paper_available(attempt)
        question = pack.question(question_id)
        metadata = (
            f'<span class="badge">{html.escape(question.kind)}</span>'
            f'<span class="badge">difficulty {question.difficulty}/5</span>'
            f'<span class="badge">{html.escape(question.track)}</span>'
            + "".join(f'<span class="badge">{html.escape(tag)}</span>' for tag in question.tags)
        )
        files = ", ".join(f"<code>{html.escape(path)}</code>" for path in question.submission_files)
        editor_control = ""
        if attempt.editor == "code" and attempt.state is AttemptState.WORKING:
            editor_control = (
                f'<form method="post" action="{self.base_path}/reopen-code">'
                '<button class="btn" type="submit">Open VSC</button></form>'
            )
        content = f"""
<section class="exam-section paper-question" id="question-{html.escape(question.id, quote=True)}">
<header class="section-heading"><h2>{html.escape(question.title)} <small>({question.points} marks)</small></h2></header>
<p>{metadata}</p>
<p><strong>Marks:</strong> {question.points} · <strong>Submission:</strong> {files}</p>
<article class="question-prompt">{markdown_to_html(pack.question_prompt(question))}</article>
<div class="actions"><a class="btn" href="{self.base_path}/#question-{html.escape(question.id, quote=True)}">Back to full paper</a>{editor_control}</div>
</section>"""
        return self._layout(
            attempt=attempt,
            pack=pack,
            title=question.title,
            content=content,
            active=question.id,
        )

    def render_resource(self, index: int) -> str:
        attempt, pack = self.attempt_and_pack()
        self._require_paper_available(attempt)
        if index < 0 or index >= len(pack.resources):
            raise ValidationError("unknown local resource")
        resource = pack.resources[index]
        path = pack.root / resource.path
        text = path.read_text(encoding="utf-8")
        content = (
            '<section class="exam-section">'
            f'<header class="section-heading"><h2>{html.escape(resource.label)}</h2></header>'
            f'<article>{markdown_to_html(text)}</article></section>'
        )
        return self._layout(
            attempt=attempt,
            pack=pack,
            title=resource.label,
            content=content,
        )


class CompanionHTTPServer(ThreadingHTTPServer):
    application: CompanionApplication


class CompanionHandler(BaseHTTPRequestHandler):
    server_version = "CSEExamTTYCompanion/1"

    @property
    def application(self) -> CompanionApplication:
        return cast(CompanionHTTPServer, self.server).application

    def log_message(self, format: str, *args: object) -> None:
        path = urlsplit(self.path).path
        if path.endswith("/health") or path.endswith("/status.json"):
            return
        sys.stderr.write(f"companion: {self.address_string()} {format % args}\n")

    def _headers(self, status: HTTPStatus, *, content_type: str, length: int) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; img-src 'self' data:; "
            "form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
        )
        self.end_headers()

    def _send(self, status: HTTPStatus, body: str, *, content_type: str) -> None:
        encoded = body.encode("utf-8")
        self._headers(status, content_type=content_type, length=len(encoded))
        self.wfile.write(encoded)

    def _segments(self) -> list[str] | None:
        path = urlsplit(self.path).path
        if len(path) > 2048:
            return None
        segments = [segment for segment in path.split("/") if segment]
        if not segments or not secrets.compare_digest(segments[0], self.application.token):
            return None
        return segments[1:]

    def _origin_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        if origin is None:
            return True
        host = self.headers.get("Host", "")
        return origin == f"http://{host}"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        segments = self._segments()
        if segments is None:
            self._send(HTTPStatus.NOT_FOUND, "Not found\n", content_type="text/plain; charset=utf-8")
            return
        try:
            if not segments:
                self._send(
                    HTTPStatus.OK,
                    self.application.render_overview(),
                    content_type="text/html; charset=utf-8",
                )
                return
            if segments == ["health"]:
                self._send(
                    HTTPStatus.OK,
                    json.dumps({"ok": True, "attempt_id": self.application.attempt_id}),
                    content_type="application/json; charset=utf-8",
                )
                return
            if segments == ["status.json"]:
                self._send(
                    HTTPStatus.OK,
                    json.dumps(self.application.status_document(), sort_keys=True),
                    content_type="application/json; charset=utf-8",
                )
                return
            if segments == ["report"]:
                self._send(
                    HTTPStatus.OK,
                    self.application.render_report(),
                    content_type="text/html; charset=utf-8",
                )
                return
            if len(segments) == 2 and segments[0] == "question":
                self._send(
                    HTTPStatus.OK,
                    self.application.render_question(segments[1]),
                    content_type="text/html; charset=utf-8",
                )
                return
            if len(segments) == 2 and segments[0] == "resource":
                self._send(
                    HTTPStatus.OK,
                    self.application.render_resource(int(segments[1])),
                    content_type="text/html; charset=utf-8",
                )
                return
        except (CSETTYError, OSError, UnicodeError, ValueError) as exc:
            message = exc.message if isinstance(exc, CSETTYError) else str(exc)
            self._send(
                HTTPStatus.BAD_REQUEST,
                self.application.render_overview(message=message, error=True),
                content_type="text/html; charset=utf-8",
            )
            return
        self._send(HTTPStatus.NOT_FOUND, "Not found\n", content_type="text/plain; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        segments = self._segments()
        if segments != ["reopen-code"] or not self._origin_allowed():
            self._send(HTTPStatus.NOT_FOUND, "Not found\n", content_type="text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = _MAX_REQUEST_BYTES + 1
        if length < 0 or length > _MAX_REQUEST_BYTES:
            self._send(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                "Request too large\n",
                content_type="text/plain; charset=utf-8",
            )
            return
        if length:
            self.rfile.read(length)
        try:
            message = self.application.reopen_code()
            body = self.application.render_overview(message=message)
            status = HTTPStatus.OK
        except CSETTYError as exc:
            body = self.application.render_overview(message=exc.message, error=True)
            status = HTTPStatus.CONFLICT
        self._send(status, body, content_type="text/html; charset=utf-8")


def serve_companion(paths: AppPaths, attempt_id: str) -> None:
    paths.ensure()
    store = Store(paths)
    attempt = store.get_attempt(attempt_id)
    runtime = DockerRuntime(paths)
    vscode = VSCodeManager(paths, runtime)
    token = secrets.token_urlsafe(32)
    server = CompanionHTTPServer(("127.0.0.1", 0), CompanionHandler)
    server.daemon_threads = True
    server.application = CompanionApplication(
        paths=paths,
        store=store,
        runtime=runtime,
        vscode=vscode,
        attempt_id=attempt.id,
        token=token,
    )
    port = int(server.server_address[1])
    info = {
        "schema_version": 1,
        "attempt_id": attempt.id,
        "pid": os.getpid(),
        "port": port,
        "token": token,
        "started_at": datetime.now(UTC).isoformat(),
    }
    atomic_write(
        _manifest_path(paths, attempt.id),
        (json.dumps(info, indent=2, sort_keys=True) + "\n").encode(),
    )
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        server.server_close()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m csetty.companion")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--attempt", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not args.serve:
        raise SystemExit("--serve is required")
    serve_companion(AppPaths.discover(args.state_dir), args.attempt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
