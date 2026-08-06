from __future__ import annotations

import json
import os
import threading
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_pack import make_pack

import csetty.companion as companion_module
from csetty.companion import (
    CompanionApplication,
    CompanionHandler,
    CompanionHTTPServer,
    CompanionInfo,
    launch_companion,
)
from csetty.course_resources import course_resource_links
from csetty.errors import StateError, ToolUnavailableError
from csetty.models import AttemptMode, AttemptState, WorkspaceKind
from csetty.pack import load_pack
from csetty.paths import AppPaths
from csetty.report import open_report_in_browser
from csetty.storage import Store
from csetty.web_render import markdown_to_html
from csetty.web_theme import THEME_NAME, theme_style


def _application(
    tmp_path: Path,
    *,
    editor: str = "code",
    state: AttemptState = AttemptState.WORKING,
    profile: str = "comp1511",
) -> tuple[CompanionApplication, Store, str]:
    root = make_pack(tmp_path / "pack")
    (root / "paper" / "q1.md").write_text(
        "# Detailed question\n\n## Background\n\nUse `<safe>`.\n",
        encoding="utf-8",
    )
    manifest = root / "pack.toml"
    manifest_text = manifest.read_text(encoding="utf-8").replace(
        'kind = "c_program"',
        'kind = "c_program"\nprompt = "paper/q1.md"\n'
        'difficulty = 2\ntrack = "normal"\ntags = ["arrays-1d"]',
    )
    if state is AttemptState.READING:
        manifest_text = manifest_text.replace(
            "reading_time_seconds = 0", "reading_time_seconds = 600"
        )
    if profile == "comp1521":
        manifest_text = (
            manifest_text.replace('course = "COMP1511"', 'course = "COMP1521"')
            .replace('profile = "comp1511"', 'profile = "comp1521"')
            .replace("csetty/comp1511:dev", "csetty/comp1521:dev")
        )
    manifest.write_text(manifest_text, encoding="utf-8")
    pack = load_pack(root)
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    now = datetime.now(UTC)
    attempt = store.create_attempt(
        pack_id=pack.id,
        pack_version=pack.version,
        pack_path=pack.root,
        pack_digest=pack.digest,
        course=pack.course,
        profile=pack.profile,
        mode=AttemptMode.EXAM,
        timed=True,
        created_at=now,
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="test-volume",
        image=pack.environment.image,
        editor=editor,
        candidate_id="z1234567",
    )
    if state is AttemptState.READING:
        attempt = store.transition(attempt.id, AttemptState.READING, at=now)
    else:
        attempt = store.transition(
            attempt.id,
            AttemptState.WORKING,
            at=now,
            deadline_at=now + timedelta(hours=3),
        )
    application = CompanionApplication(
        paths=paths,
        store=store,
        runtime=object(),  # type: ignore[arg-type]
        vscode=object(),  # type: ignore[arg-type]
        attempt_id=attempt.id,
        token="t" * 43,
        reopen_callback=lambda: "VS Code reopen requested.",
    )
    return application, store, attempt.id


def test_companion_overview_and_question_are_pack_driven(tmp_path: Path) -> None:
    application, _store, _attempt_id = _application(tmp_path)
    overview = application.render_overview()
    question = application.render_question("q1")
    assert "Open VSC" in overview
    assert "not made or managed by UNSW" in overview
    assert "Course home and complete index" in overview
    assert "Detailed question" in question
    assert "difficulty 2/5" in question
    assert "arrays-1d" in question
    assert "&lt;safe&gt;" in question
    assert overview.count('target="_blank" rel="noopener noreferrer"') == len(
        course_resource_links("comp1511")
    )
    assert theme_style() in overview
    assert f'data-csetty-theme="{THEME_NAME}"' in question
    assert f'data-csetty-theme-script="{THEME_NAME}"' in overview
    assert 'class="course-comp1511"' in overview


def test_companion_cold_start_can_become_healthy_after_ten_seconds(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _application_instance, store, attempt_id = _application(tmp_path)
    attempt = store.get_attempt(attempt_id)
    elapsed = {"seconds": 0.0}
    expected = CompanionInfo(
        attempt_id=attempt_id,
        pid=43210,
        port=32123,
        token="t" * 43,
        started_at=datetime.now(UTC).isoformat(),
    )
    monkeypatch.setattr(
        companion_module,
        "_read_info",
        lambda _paths, _attempt_id: expected if elapsed["seconds"] >= 12 else None,
    )
    monkeypatch.setattr(companion_module, "_healthy", lambda _info: True)
    monkeypatch.setattr(
        companion_module.subprocess,
        "Popen",
        lambda *_args, **_kwargs: SimpleNamespace(poll=lambda: None),
    )
    monkeypatch.setattr(
        companion_module.time, "monotonic", lambda: elapsed["seconds"]
    )
    monkeypatch.setattr(
        companion_module.time,
        "sleep",
        lambda _seconds: elapsed.__setitem__("seconds", elapsed["seconds"] + 1),
    )

    assert launch_companion(store.paths, attempt, open_browser=False) == expected
    assert elapsed["seconds"] == 12


def test_companion_runs_ready_callback_after_opening_existing_page(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _application_instance, store, attempt_id = _application(tmp_path)
    attempt = store.get_attempt(attempt_id)
    expected = CompanionInfo(
        attempt_id=attempt_id,
        pid=os.getpid(),
        port=32123,
        token="t" * 43,
        started_at=datetime.now(UTC).isoformat(),
    )
    events: list[str] = []
    monkeypatch.setattr(companion_module, "_read_info", lambda *_args: expected)
    monkeypatch.setattr(companion_module, "_healthy", lambda _info: True)

    assert (
        launch_companion(
            store.paths,
            attempt,
            ready_callback=lambda: events.append("ready"),
            browser_open=lambda _url: events.append("open"),
        )
        == expected
    )
    assert events == ["open", "ready"]


def test_companion_does_not_start_reading_when_browser_open_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _application_instance, store, attempt_id = _application(tmp_path)
    attempt = store.get_attempt(attempt_id)
    expected = CompanionInfo(
        attempt_id=attempt_id,
        pid=os.getpid(),
        port=32123,
        token="t" * 43,
        started_at=datetime.now(UTC).isoformat(),
    )
    events: list[str] = []
    monkeypatch.setattr(companion_module, "_read_info", lambda *_args: expected)
    monkeypatch.setattr(companion_module, "_healthy", lambda _info: True)

    with pytest.raises(ToolUnavailableError, match="reading time has not started"):
        launch_companion(
            store.paths,
            attempt,
            ready_callback=lambda: events.append("ready"),
            browser_open=lambda _url: False,
        )

    assert events == []


def test_companion_process_creation_failure_removes_startup_lock(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _application_instance, store, attempt_id = _application(tmp_path)
    attempt = store.get_attempt(attempt_id)
    monkeypatch.setattr(companion_module, "_read_info", lambda *_args: None)

    def fail_to_start(*_args: object, **_kwargs: object) -> None:
        raise OSError("process creation failed")

    monkeypatch.setattr(companion_module.subprocess, "Popen", fail_to_start)

    with pytest.raises(ToolUnavailableError, match="process creation failed"):
        launch_companion(store.paths, attempt, open_browser=False)
    assert not (store.paths.attempts / attempt_id / "companion.starting").exists()


def test_companion_status_tracks_latest_submission(tmp_path: Path) -> None:
    application, store, attempt_id = _application(tmp_path)
    store.record_submission(
        attempt_id=attempt_id,
        question_id="q1",
        files={"q1.c": b"int main(void) { return 0; }\n"},
        created_at=datetime.now(UTC),
    )
    status = application.status_document()
    assert status["state"] == "WORKING"
    assert status["questions"] == [{"id": "q1", "submitted": True, "sequence": 1}]


def test_reading_companion_shows_full_prompt_without_editor_or_external_resources(
    tmp_path: Path,
) -> None:
    application, _store, _attempt_id = _application(tmp_path, state=AttemptState.READING)
    overview = application.render_overview()
    question = application.render_question("q1")
    status = application.status_document()

    assert "read-only exam paper" in overview
    assert "Reading time remaining" in overview
    assert "Locked during reading time" in overview
    assert "workspace and editor remain locked" in overview
    assert "Open VSC" not in overview
    assert 'target="_blank" rel="noopener noreferrer"' not in overview
    assert 'data-state="READING"' in overview
    assert "/status.json" in overview
    assert overview.count('class="timer" data-countdown') == 1
    assert overview.count("<span data-countdown>") == 1
    assert "setTimeout(pollLoop, 1000)" in overview
    assert "Detailed question" in question
    assert "Detailed question" in overview
    assert '<article class="question-prompt">' in overview
    assert 'id="question-q1"' in overview
    assert "Use <code>&lt;safe&gt;</code>." in question
    assert status["state"] == "READING"
    assert status["remaining_seconds"] is not None
    assert 0 <= status["remaining_seconds"] <= 600


def test_comp1521_companion_uses_the_teal_course_variant(tmp_path: Path) -> None:
    application, _store, _attempt_id = _application(tmp_path, profile="comp1521")
    overview = application.render_overview()

    assert 'class="course-comp1521"' in overview
    assert "COMP1521 — CSEExamTTY" in overview
    assert "--course-accent: #42a097" in overview
    assert theme_style() in overview


def test_reopen_callback_is_invoked(tmp_path: Path) -> None:
    application, _store, _attempt_id = _application(tmp_path)
    assert application.reopen_code() == "VS Code reopen requested."


def test_terminal_companion_does_not_offer_unusable_vscode_recovery(tmp_path: Path) -> None:
    application, _store, _attempt_id = _application(tmp_path, editor="terminal")
    overview = application.render_overview()
    question = application.render_question("q1")
    assert "Open VSC" not in overview
    assert "Open VSC" not in question
    assert "csetty resume" in overview


def test_finished_companion_does_not_offer_unusable_vscode_recovery(tmp_path: Path) -> None:
    application, store, attempt_id = _application(tmp_path)
    store.transition(
        attempt_id,
        AttemptState.FINISHED,
        at=datetime.now(UTC),
        finish_reason="student",
    )
    overview = application.render_overview()
    question = application.render_question("q1")
    assert "Open VSC" not in overview
    assert "Open VSC" not in question
    assert "recovery is unavailable because this attempt is FINISHED" in overview
    assert "Preparing final report" in overview
    assert "Open final report" not in overview


def test_finished_companion_serves_and_advertises_the_durable_report(tmp_path: Path) -> None:
    application, store, attempt_id = _application(tmp_path)
    store.transition(
        attempt_id,
        AttemptState.FINISHED,
        at=datetime.now(UTC),
        finish_reason="student",
    )
    report = store.paths.reports / f"{attempt_id}.html"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("<!doctype html><title>Final report</title>", encoding="utf-8")

    assert application.status_document()["report_ready"] is True
    assert application.render_report() == "<!doctype html><title>Final report</title>"
    overview = application.render_overview()
    assert 'data-report-url="/' in overview
    assert "Open final report" in overview


def test_report_opener_uses_the_live_companion_http_route(tmp_path: Path) -> None:
    application, store, attempt_id = _application(tmp_path)
    store.transition(
        attempt_id,
        AttemptState.FINISHED,
        at=datetime.now(UTC),
        finish_reason="student",
    )
    report = store.paths.reports / f"{attempt_id}.html"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("<!doctype html><title>Final report</title>", encoding="utf-8")

    try:
        server = CompanionHTTPServer(("127.0.0.1", 0), CompanionHandler)
    except PermissionError:
        pytest.skip("loopback sockets are unavailable in this test sandbox")
    server.daemon_threads = True
    server.application = application
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    port = int(server.server_address[1])
    manifest = store.paths.attempts / attempt_id / "companion.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "attempt_id": attempt_id,
                "pid": os.getpid(),
                "port": port,
                "token": application.token,
                "started_at": datetime.now(UTC).isoformat(),
            }
        ),
        encoding="utf-8",
    )
    opened: list[str] = []
    expected = f"http://127.0.0.1:{port}/{application.token}/report"
    try:
        assert open_report_in_browser(
            report,
            browser_open=lambda url: opened.append(url) is None,
        )
        assert opened == [expected]
        with urllib.request.urlopen(expected, timeout=2) as response:
            assert response.read().decode() == "<!doctype html><title>Final report</title>"
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=2)


def test_finished_companion_rejects_reopen_before_callback(tmp_path: Path) -> None:
    application, store, attempt_id = _application(tmp_path)
    store.transition(
        attempt_id,
        AttemptState.FINISHED,
        at=datetime.now(UTC),
        finish_reason="student",
    )
    with pytest.raises(
        StateError,
        match="^VS Code is unavailable while attempt is FINISHED$",
    ):
        application.reopen_code()


def test_markdown_renderer_does_not_allow_raw_html() -> None:
    rendered = markdown_to_html("# Title\n\n<script>alert(1)</script>\n\n`<tag>`")
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "<code>&lt;tag&gt;</code>" in rendered


def test_resource_catalogs_cover_course_indexes_and_core_guides() -> None:
    comp1511 = course_resource_links("comp1511")
    comp1521 = course_resource_links("comp1521")
    assert any(item.label == "Course home and complete index" for item in comp1511)
    assert any(item.label == "Debugging guide" for item in comp1511)
    assert any(item.label == "Week 02 lecture code" for item in comp1511)
    assert any(item.label == "Week 02 laboratory sample solutions" for item in comp1511)
    assert any(item.label == "Week 10 lecture recording B" for item in comp1511)
    assert any(item.label == "Practice exam solutions" for item in comp1511)
    assert any(item.label == "Revision videos" for item in comp1511)
    assert any(item.label == "MIPS instruction set" for item in comp1521)
    assert any(item.label == "mipsy web" for item in comp1521)
    assert any(item.label == "Unicode notes" for item in comp1521)
    assert any(item.label == "Unicode code" for item in comp1521)
    assert any(item.label == "Week 10 lecture slides" for item in comp1521)
    assert any(item.label == "Week 03 weekly-test sample answers" for item in comp1521)


def test_resource_catalogs_are_unique_https_links_without_real_submission_actions() -> None:
    for profile in ("comp1511", "comp1521"):
        links = course_resource_links(profile)
        urls = [item.url for item in links]
        assert len(urls) == len(set(urls))
        assert all(url.startswith("https://") for url in urls)
        assert all("/~give/" not in url and "/student/" not in url for url in urls)
