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
from datetime import UTC, datetime
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

_MAX_REQUEST_BYTES = 4096
_START_TIMEOUT_SECONDS = 10.0


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
) -> CompanionInfo:
    """Start or reuse the loopback-only page for an attempt."""
    existing = _read_info(paths, attempt.id)
    if existing is not None and _healthy(existing):
        if open_browser:
            browser_open(existing.url)
        return existing

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
            subprocess.Popen(
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

    deadline = time.monotonic() + _START_TIMEOUT_SECONDS
    try:
        while time.monotonic() < deadline:
            info = _read_info(paths, attempt.id)
            if info is not None and _healthy(info):
                if open_browser:
                    browser_open(info.url)
                return info
            time.sleep(0.05)
    finally:
        if owns_lock:
            lock.unlink(missing_ok=True)
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
    def _remaining_seconds(attempt: Attempt) -> int | None:
        if attempt.deadline_at is None:
            return None
        return max(0, int((attempt.deadline_at - datetime.now(UTC)).total_seconds()))

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
            "remaining_seconds": self._remaining_seconds(attempt),
            "deadline_at": (
                None if attempt.deadline_at is None else attempt.deadline_at.isoformat()
            ),
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
            selected = ' aria-current="page" class="active"' if question.id == active else ""
            question_items.append(
                f'<li><a{selected} href="{self.base_path}/question/{html.escape(question.id)}">'
                f"Q{index}. {html.escape(question.title)}</a></li>"
            )
        return (
            f'<a class="home-link" href="{self.base_path}/">Exam overview</a>'
            f'<ol class="question-nav">{"".join(question_items)}</ol>'
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
        remaining = self._remaining_seconds(attempt)
        timer = self._remaining_text(remaining)
        message_html = ""
        if message:
            message_html = (
                f'<div class="message {"error" if error else "success"}">'
                f"{html.escape(message)}</div>"
            )
        deadline = "" if attempt.deadline_at is None else attempt.deadline_at.isoformat()
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{html.escape(title)} — CSEExamTTY</title>
<style>
:root {{ --ink:#17253d; --nav:#132a4a; --accent:#f2b134; --paper:#fff; --muted:#607086; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; color:var(--ink); background:#edf1f5; font:16px/1.55 system-ui,sans-serif; }}
header {{ background:var(--nav); color:white; border-bottom:6px solid var(--accent); padding:1rem 1.5rem; }}
header h1 {{ margin:0; font-size:1.45rem; }}
header p {{ margin:.25rem 0 0; opacity:.88; }}
.status {{ display:flex; gap:1rem; align-items:center; flex-wrap:wrap; margin-top:.75rem; }}
.timer {{ font:700 1.25rem ui-monospace,monospace; background:#071a31; padding:.35rem .65rem; border-radius:.25rem; }}
.shell {{ display:grid; grid-template-columns:minmax(230px,300px) minmax(0,1fr); min-height:calc(100vh - 130px); }}
nav {{ background:#f8fafc; border-right:1px solid #c9d2dc; padding:1rem; overflow:auto; }}
nav a {{ color:#173e6d; text-decoration:none; }}
nav a:hover, nav a.active {{ color:#8a4d00; text-decoration:underline; }}
.home-link {{ display:block; font-weight:700; margin-bottom:.75rem; }}
.question-nav {{ margin:0; padding-left:1.35rem; }}
.question-nav li {{ margin:.35rem 0; }}
main {{ min-width:0; padding:1.5rem; }}
.card {{ max-width:1050px; min-width:0; margin:0 auto 1rem; background:var(--paper); border:1px solid #d3dae2; border-radius:.35rem; padding:1.35rem; box-shadow:0 2px 8px #17253d12; overflow-x:auto; }}
.notice {{ border-left:5px solid var(--accent); background:#fff7df; }}
.message {{ max-width:1050px; margin:0 auto 1rem; padding:.85rem 1rem; border-radius:.3rem; }}
.success {{ background:#e6f7eb; border:1px solid #65a878; }}
.error {{ background:#fff0f0; border:1px solid #c66; }}
.actions {{ display:flex; gap:.75rem; flex-wrap:wrap; margin:1rem 0; }}
button,.button {{ appearance:none; border:0; border-radius:.25rem; padding:.65rem .9rem; background:#1d568f; color:white; font-weight:700; cursor:pointer; text-decoration:none; }}
button:hover,.button:hover {{ background:#123d69; }}
table {{ width:100%; border-collapse:collapse; }}
th,td {{ padding:.55rem; border-bottom:1px solid #d5dce4; text-align:left; vertical-align:top; }}
th {{ background:#f1f4f7; }}
code {{ background:#eef1f4; padding:.08rem .25rem; border-radius:.2rem; overflow-wrap:anywhere; }}
pre {{ overflow:auto; background:#101b2b; color:#f5f7fa; padding:1rem; border-radius:.3rem; }}
pre code {{ background:transparent; padding:0; }}
.badge {{ display:inline-block; border-radius:999px; background:#e5edf6; margin:.12rem .2rem .12rem 0; padding:.15rem .5rem; font-size:.82rem; }}
.resource-grid {{ columns:2 280px; column-gap:2rem; }}
.resource-section {{ break-inside:avoid; margin-bottom:1rem; }}
.resource-section h3 {{ margin-bottom:.25rem; }}
.resource-section ul {{ margin-top:.25rem; }}
.muted {{ color:var(--muted); }}
@media (max-width:760px) {{ .shell {{ grid-template-columns:1fr; }} nav {{ border-right:0; border-bottom:1px solid #c9d2dc; max-height:34vh; }} main {{ padding:.8rem; }} }}
</style>
</head>
<body data-deadline="{html.escape(deadline, quote=True)}">
<header>
<h1>{html.escape(pack.course)} local exam workspace</h1>
<p>{html.escape(pack.title)} · not made or managed by UNSW</p>
<div class="status"><span>State: <strong>{html.escape(attempt.state.value)}</strong></span><span>Remaining: <span class="timer" id="timer">{timer}</span></span></div>
</header>
<div class="shell">
<nav aria-label="Question navigation">{self._navigation(pack, active)}</nav>
<main>{message_html}{content}</main>
</div>
<script>
(() => {{
  const deadline = document.body.dataset.deadline;
  const timer = document.getElementById('timer');
  if (!deadline || !timer) return;
  const update = () => {{
    const seconds = Math.max(0, Math.floor((Date.parse(deadline) - Date.now()) / 1000));
    const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const s = String(seconds % 60).padStart(2, '0');
    timer.textContent = `${{h}}:${{m}}:${{s}}`;
  }};
  update(); setInterval(update, 1000);
}})();
</script>
</body>
</html>"""

    def _resource_sections(self, pack: Pack) -> str:
        sections: dict[str, list[CourseResourceLink]] = {}
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
        latest = {
            submission["question_id"]: submission
            for submission in self.store.list_submissions(attempt.id)
        }
        rows = []
        for index, question in enumerate(pack.questions, start=1):
            submission = latest.get(question.id)
            status = "Not submitted" if submission is None else f"Submitted #{submission['sequence']}"
            tags = "".join(f'<span class="badge">{html.escape(tag)}</span>' for tag in question.tags)
            rows.append(
                "<tr>"
                f'<td><a href="{self.base_path}/question/{html.escape(question.id)}">Q{index}</a></td>'
                f"<td>{html.escape(question.title)}<br>{tags}</td>"
                f"<td>{question.points}</td><td>{html.escape(question.track)}</td>"
                f"<td>{html.escape(status)}</td></tr>"
            )
        if attempt.editor == "code" and attempt.state is AttemptState.WORKING:
            editor_control = (
                f'<form method="post" action="{self.base_path}/reopen-code">'
                '<button type="submit">Open VSC</button></form>'
            )
            editor_text = (
                "Use this recovery control to reconnect to the existing supervised Docker "
                "container; it does not create a new attempt."
            )
        elif attempt.editor == "code":
            editor_control = ""
            editor_text = (
                f"VS Code recovery is unavailable because this attempt is "
                f"{attempt.state.value}."
            )
        else:
            editor_control = ""
            editor_text = "This attempt uses terminal mode. Run csetty resume to reopen its terminal."
        content = f"""
<section class="card notice">
<h2>Local simulation notice</h2>
<p>This original mock exam system is not made or managed by the UNSW School of Computer Science and Engineering. Submissions remain on this computer and are not sent to UNSW.</p>
</section>
<section class="card">
<h2>Exam controls</h2>
<p>Closing the editor does not stop the clock. {editor_text}</p>
<div class="actions">{editor_control}</div>
</section>
<section class="card">
<h2>Questions</h2>
<table><thead><tr><th>#</th><th>Question</th><th>Marks</th><th>Track</th><th>Submission</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
</section>
<section class="card">
<h2>Course resources</h2>
<p class="muted">Bundled resources are available offline. Official public links are an index only: their content is not copied into CSEExamTTY and requires host network access. Docker remains subject to the attempt network policy.</p>
<div class="resource-grid">{self._resource_sections(pack)}</div>
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
                '<button type="submit">Open VSC</button></form>'
            )
        content = f"""
<section class="card">
<p>{metadata}</p>
<p><strong>Marks:</strong> {question.points} · <strong>Submission:</strong> {files}</p>
<article>{markdown_to_html(pack.question_prompt(question))}</article>
<div class="actions"><a class="button" href="{self.base_path}/">Back to overview</a>{editor_control}</div>
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
        if index < 0 or index >= len(pack.resources):
            raise ValidationError("unknown local resource")
        resource = pack.resources[index]
        path = pack.root / resource.path
        text = path.read_text(encoding="utf-8")
        content = f'<section class="card"><article>{markdown_to_html(text)}</article></section>'
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
        sys.stderr.write(f"companion: {self.address_string()} {format % args}\n")

    def _headers(self, status: HTTPStatus, *, content_type: str, length: int) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
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
