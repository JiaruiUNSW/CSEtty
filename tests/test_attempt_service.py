from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_pack import make_pack

from csetty.clock import FrozenClock
from csetty.errors import StateError, ValidationError
from csetty.models import AttemptMode, AttemptState, WorkspaceKind
from csetty.pack import Pack, load_pack, snapshot_pack
from csetty.pack import TestGroup as PackTestGroup
from csetty.paths import AppPaths
from csetty.storage import Store
from csetty.supervisor import AttemptService, _question_alias, _resolve_question


class RuntimeFake:
    def __init__(self, workspace: dict[str, bytes]) -> None:
        self.workspace = workspace
        self.judged_contents: list[bytes] = []

    def read_workspace_files(self, _attempt, paths) -> dict[str, bytes]:
        return {path: self.workspace[path] for path in paths}

    def write_workspace_file(self, _attempt, path: str, content: bytes, *, overwrite: bool) -> str:
        if path in self.workspace and not overwrite:
            return "kept"
        self.workspace[path] = content
        return "restored"

    def run_judge(
        self,
        *,
        attempt,
        pack: Pack,
        question,
        snapshot: Path,
        groups: tuple[PackTestGroup, ...],
    ) -> dict[str, object]:
        del attempt, pack
        content = (snapshot / question.submission_files[0]).read_bytes()
        self.judged_contents.append(content)
        passed = b"pass" in content
        result_class = "PASS" if passed else "WRONG_OUTPUT"
        rendered_groups = []
        for group in groups:
            rendered_groups.append(
                {
                    "id": group.id,
                    "visibility": group.visibility.value,
                    "tests": [
                        {
                            "id": test.id,
                            "argv": list(test.argv),
                            "stdin": test.stdin,
                            "expected_stdout": test.expected_stdout,
                            "expected_stderr": test.expected_stderr,
                            "result": result_class,
                            "duration_ms": 1,
                            "exit_code": 0,
                            "stdout": "" if passed else "wrong\n",
                            "stderr": "",
                            "detail": "" if passed else "stdout did not match (exact)",
                        }
                        for test in group.tests
                    ],
                }
            )
        return {
            "status": "PASS" if passed else "FAIL",
            "build": None,
            "build_argv": list(question.build_argv),
            "groups": rendered_groups,
        }


def make_service(tmp_path: Path, now: datetime) -> tuple[AttemptService, Store, RuntimeFake]:
    source = load_pack(make_pack(tmp_path / "source-pack"))
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    attempt_id = "00000000-0000-4000-8000-000000000001"
    pack = snapshot_pack(source, paths.attempts / attempt_id / "pack")
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
        workspace_ref="service-volume",
        image="csetty/comp1511:dev",
        attempt_id=attempt_id,
        candidate_id="z1234567",
    )
    attempt = store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=now,
        deadline_at=now + timedelta(minutes=10),
    )
    runtime = RuntimeFake({"q1.c": b"pass\n"})
    service = AttemptService(
        store=store,
        runtime=runtime,  # type: ignore[arg-type]
        attempt=attempt,
        pack=pack,
        clock=FrozenClock(now),
    )
    return service, store, runtime


def test_autotest_does_not_submit_and_final_grade_uses_submission_snapshot(
    tmp_path: Path,
) -> None:
    now = datetime(2026, 8, 5, tzinfo=UTC)
    service, store, runtime = make_service(tmp_path, now)

    autotest = service.handle(
        {"operation": "autotest", "arguments": {"activity": "q1", "selector": None}}
    )
    assert autotest["exit_code"] == 0
    assert store.list_submissions(service.attempt_id) == []

    submitted = service.handle(
        {"operation": "submit", "arguments": {"activity": "q1", "files": ["q1.c"]}}
    )
    assert submitted["exit_code"] == 0
    assert submitted["stdout"] == "Your answer (q1.c) for q1 has been submitted.\n"

    checked = service.handle({"operation": "check", "arguments": {}})
    assert checked["stdout"] == "You have submissions for following questions:\nq1\n"

    shown = service.handle(
        {"operation": "submission", "arguments": {"activity": "q1"}}
    )
    assert shown["exit_code"] == 0
    assert shown["stdout"] == (
        "Submission for q1\n"
        "Submitted by: z1234567\n"
        "Submitted at: 2026-08-05T00:00:00Z\n"
        "\n"
        "File: q1.c\n"
        "   1  pass\n"
    )
    runtime.workspace["q1.c"] = b"fail after submission\n"

    finished = service.handle({"operation": "finish", "arguments": {}})
    assert finished["exit_code"] == 0
    grade = store.get_grade(service.attempt_id)
    assert grade is not None
    assert grade["report"]["score"]["earned"] == 10
    assert runtime.judged_contents[-1] == b"pass\n"
    assert store.get_attempt(service.attempt_id).state is AttemptState.FINISHED


def test_check_and_show_submission_when_nothing_was_submitted(tmp_path: Path) -> None:
    now = datetime(2026, 8, 5, tzinfo=UTC)
    service, _store, _runtime = make_service(tmp_path, now)

    checked = service.handle({"operation": "check", "arguments": {}})
    assert checked["stdout"] == "You have submissions for following questions:\n(none)\n"

    shown = service.handle(
        {"operation": "submission", "arguments": {"activity": "q1"}}
    )
    assert shown == {
        "exit_code": 1,
        "stdout": "",
        "stderr": "No submission found for q1.\n",
    }


def test_q_number_alias_resolves_prefixed_pack_activity(tmp_path: Path) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
    prefixed = replace(pack, questions=(replace(pack.questions[0], id="prac_q1"),))

    question = _resolve_question(prefixed, "q1")
    assert question.id == "prac_q1"
    assert _question_alias(prefixed, question) == "q1"


def test_deadline_rejects_late_operation_and_expires_attempt(tmp_path: Path) -> None:
    now = datetime(2026, 8, 5, tzinfo=UTC)
    service, store, _runtime = make_service(tmp_path, now)
    clock = service.clock
    assert isinstance(clock, FrozenClock)
    clock.advance(seconds=10 * 60)

    with pytest.raises(StateError, match="EXPIRED"):
        service.handle({"operation": "submit", "arguments": {"activity": "q1", "files": ["q1.c"]}})
    assert store.get_attempt(service.attempt_id).state is AttemptState.EXPIRED


def test_supervisor_rejects_a_tampered_attempt_pack(tmp_path: Path) -> None:
    now = datetime(2026, 8, 5, tzinfo=UTC)
    service, store, _runtime = make_service(tmp_path, now)
    attempt = store.get_attempt(service.attempt_id)
    paper = Path(attempt.pack_path) / "paper" / "index.md"
    paper.chmod(0o644)
    paper.write_text("tampered\n", encoding="utf-8")

    with pytest.raises(ValidationError, match="snapshot changed"):
        service.handle({"operation": "status", "arguments": {}})
