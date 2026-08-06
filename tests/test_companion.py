from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_pack import make_pack

from csetty.companion import CompanionApplication
from csetty.course_resources import course_resource_links
from csetty.errors import StateError
from csetty.models import AttemptMode, AttemptState, WorkspaceKind
from csetty.pack import load_pack
from csetty.paths import AppPaths
from csetty.storage import Store
from csetty.web_render import markdown_to_html


def _application(
    tmp_path: Path, *, editor: str = "code"
) -> tuple[CompanionApplication, Store, str]:
    root = make_pack(tmp_path / "pack")
    (root / "paper" / "q1.md").write_text(
        "# Detailed question\n\n## Background\n\nUse `<safe>`.\n",
        encoding="utf-8",
    )
    manifest = root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            'kind = "c_program"',
            'kind = "c_program"\nprompt = "paper/q1.md"\n'
            'difficulty = 2\ntrack = "normal"\ntags = ["arrays-1d"]',
        ),
        encoding="utf-8",
    )
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
