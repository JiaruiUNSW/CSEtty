from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest
from test_pack import make_pack

import csetty.report as report_module
from csetty.models import Attempt, AttemptMode, AttemptState, WorkspaceKind
from csetty.pack import load_pack, snapshot_author_materials
from csetty.report import (
    open_report_in_browser,
    render_report_html,
    render_report_text,
    report_document,
)
from csetty.web_theme import THEME_NAME, theme_style


def _document():
    grade = {
        "notice": "Local simulator estimate; this is not an official UNSW mark.",
        "score": {
            "earned": 5,
            "automatically_available": 8,
            "total": 10,
            "not_automatically_assessed": 2,
        },
        "questions": [
            {
                "id": "q1",
                "title": "Question <one>",
                "points_earned": 5,
                "automatic_points": 8,
                "passed": True,
                "groups": [
                    {
                        "id": "public",
                        "visibility": "public",
                        "passed": True,
                        "points_earned": 5,
                        "points_available": 5,
                    }
                ],
            }
        ],
        "hurdles": [{"label": "Core hurdle", "passed": True}],
    }
    return {
        "notice": "CSEExamTTY local simulation; no submission was sent to UNSW.",
        "attempt": {
            "id": "attempt",
            "pack": "pack@1.0.0",
            "course": "COMP1511",
            "profile": "comp1511",
            "candidate_id": "z1234567",
            "state": "FINISHED",
            "mode": "exam",
            "image": "csetty/comp1511:dev",
            "toolchain": {"image": {"id": "sha256:test"}, "tools": {}},
        },
        "submissions": [{"question_id": "q1", "sequence": 2, "manifest_digest": "a" * 64}],
        "grade": grade,
    }


def test_terminal_and_html_reports_include_groups_hurdles_and_hashes() -> None:
    document = _document()
    text = render_report_text(document)
    page = render_report_html(document)
    assert "q1: 5/8 automatic points" in text
    assert "Core hurdle: PASS" in text
    assert "public [public]: PASS" in text
    assert "a" * 64 in page
    assert "Core hurdle: PASS" in page
    assert "public" in page
    assert "Question &lt;one&gt;" in page
    assert theme_style() in page
    assert f'data-csetty-theme="{THEME_NAME}"' in page
    assert f'data-csetty-theme-script="{THEME_NAME}"' in page
    assert 'class="course-comp1511"' in page


def test_comp1521_report_uses_the_same_teal_course_theme() -> None:
    document = _document()
    document["attempt"]["course"] = "COMP1521"
    document["attempt"]["profile"] = "comp1521"
    document["attempt"]["image"] = "csetty/comp1521:dev"

    page = render_report_html(document)

    assert 'class="course-comp1521"' in page
    assert "COMP1521 — CSEExamTTY" in page
    assert "--course-accent: #42a097" in page
    assert theme_style() in page


def test_completed_html_report_opens_as_a_local_file_url(tmp_path: Path) -> None:
    html_path = tmp_path / "attempt report.html"
    html_path.write_text("<html></html>", encoding="utf-8")
    opened: list[str] = []

    assert open_report_in_browser(
        html_path,
        browser_open=lambda url: opened.append(url) is None,
    )
    assert opened == [html_path.resolve().as_uri()]


def test_completed_html_report_prefers_the_healthy_companion_url(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    html_path = tmp_path / "reports" / "attempt-id.html"
    html_path.parent.mkdir()
    html_path.write_text("<html></html>", encoding="utf-8")
    opened: list[str] = []
    monkeypatch.setattr(
        report_module,
        "_companion_report_url",
        lambda _path: "http://127.0.0.1:43210/token/report",
    )

    assert open_report_in_browser(
        html_path,
        browser_open=lambda url: opened.append(url) is None,
    )
    assert opened == ["http://127.0.0.1:43210/token/report"]


def test_missing_html_report_is_not_sent_to_the_browser(tmp_path: Path) -> None:
    opened: list[str] = []
    assert not open_report_in_browser(
        tmp_path / "missing.html",
        browser_open=lambda url: opened.append(url) is None,
    )
    assert opened == []


def test_full_report_embeds_submission_evaluation_and_terminal_solution(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    (root / "paper" / "q1.md").write_text("# Task\n\nDetailed prompt.\n", encoding="utf-8")
    manifest = root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            'kind = "c_program"',
            'kind = "c_program"\nprompt = "paper/q1.md"\n'
            'difficulty = 2\ntrack = "normal"\ntags = ["debugging", "loops", "functions"]',
        ),
        encoding="utf-8",
    )
    (root / "solutions" / "explanations").mkdir(parents=True)
    (root / "solutions" / "reference").mkdir()
    (root / "solutions" / "explanations" / "q1.md").write_text(
        "# Worked solution\n\nUse a direct return.\n", encoding="utf-8"
    )
    (root / "solutions" / "reference" / "q1.c").write_text(
        "int main(void) { return 0; }\n", encoding="utf-8"
    )
    pack = load_pack(root)
    author_root = tmp_path / "attempt" / "author"
    snapshot_author_materials(pack, author_root)
    now = datetime.now(UTC)
    attempt = Attempt(
        id="attempt-id",
        pack_id=pack.id,
        pack_version=pack.version,
        pack_path=str(tmp_path / "attempt" / "pack"),
        pack_digest=pack.digest,
        course=pack.course,
        profile=pack.profile,
        mode=AttemptMode.EXAM,
        state=AttemptState.FINISHED,
        timed=True,
        created_at=now,
        reading_started_at=now,
        working_started_at=now,
        deadline_at=now,
        finished_at=now,
        finish_reason="student",
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="volume",
        image=pack.environment.image,
        provenance={},
        container_name="csetty-attempt",
        session_token="token",
        network="none",
        editor="code",
        candidate_id="z1234567",
    )
    source = b"<script>alert(1)</script>\n"
    submission = {
        "id": 1,
        "question_id": "q1",
        "sequence": 1,
        "created_at": now.isoformat(),
        "manifest_digest": "m" * 64,
        "files": [
            {
                "path": "q1.c",
                "object_digest": "o" * 64,
                "size": len(source),
            }
        ],
    }
    grade = {
        "score": {
            "earned": 0,
            "automatically_available": 10,
            "total": 10,
            "not_automatically_assessed": 0,
        },
        "questions": [
            {
                "id": "q1",
                "title": "Return success",
                "points_earned": 0,
                "automatic_points": 10,
                "total_points": 10,
                "passed": False,
                "groups": [
                    {
                        "id": "public",
                        "visibility": "public",
                        "passed": False,
                        "points_earned": 0,
                        "points_available": 5,
                        "tests": [
                            {
                                "id": "basic",
                                "result": "WRONG_OUTPUT",
                                "duration_ms": 1,
                                "detail": "stdout did not match",
                                "stdin": "",
                                "expected_stdout": "ok\n",
                                "stdout_preview": "bad\n",
                                "expected_stderr": "",
                                "stderr_preview": "",
                                "expected_exit": 0,
                                "exit_code": 3,
                            }
                        ],
                    }
                ],
            }
        ],
        "hurdles": [],
    }
    document = report_document(
        attempt=attempt,
        pack=pack,
        submissions=[submission],
        grade=grade,
        object_reader=lambda _digest: source,
        author_root=author_root,
    )
    page = render_report_html(document)
    assert document["schema_version"] == 2
    assert document["questions"][0]["submission"]["files"][0]["content"].startswith(
        "<script>"
    )
    assert document["questions"][0]["solution"]["explanation"]["content"].startswith(
        "# Worked solution"
    )
    working_document = report_document(
        attempt=replace(
            attempt,
            state=AttemptState.WORKING,
            finished_at=None,
            finish_reason=None,
        ),
        pack=pack,
        submissions=[submission],
        grade=None,
        object_reader=lambda _digest: source,
        author_root=author_root,
    )
    assert working_document["questions"][0]["solution"] is None
    assert "What still needs work" in page
    assert "WRONG_OUTPUT" in page
    assert "Expected exit status" in page
    assert "Actual exit status" in page
    assert "<pre><code>0</code></pre>" in page
    assert "<pre><code>3</code></pre>" in page
    assert "Reproduce the first failing test locally" in page
    assert (
        '<span class="badge">debugging</span> · '
        '<span class="badge">loops</span> · '
        '<span class="badge">functions</span>'
    ) in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    assert "<script>alert(1)</script>" not in page
