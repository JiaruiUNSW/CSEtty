from __future__ import annotations

import json
import threading
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_pack import make_pack

import csetty.cli as cli
import csetty.supervisor as supervisor_module
from csetty.clock import FrozenClock
from csetty.errors import StateError
from csetty.models import AttemptMode, AttemptState, WorkspaceKind
from csetty.pack import load_pack
from csetty.paths import AppPaths
from csetty.storage import Store
from csetty.supervisor import AttemptService


class RuntimeStub:
    @staticmethod
    def image_for_profile(profile: str) -> str:
        return f"csetty/{profile}:dev"

    @staticmethod
    def image_exists(_image: str) -> bool:
        return True

    @staticmethod
    def ensure_profile_ready(_profile: str) -> None:
        return None

    @staticmethod
    def profile_provenance(profile: str) -> dict[str, object]:
        return {
            "image": {"id": f"sha256:csetty/{profile}:dev"},
            "judge_image": {"id": f"sha256:csetty/{profile}-judge:dev"},
            "tools": {},
        }


def test_start_records_an_attempt_owned_pack_snapshot(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source_root = make_pack(tmp_path / "source-pack")
    (source_root / "solutions").mkdir()
    (source_root / "solutions" / "q1.c").write_text("secret", encoding="utf-8")
    source_pack = load_pack(source_root)
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    runtime = RuntimeStub()

    monkeypatch.setattr(cli.PackRepository, "get", lambda _self, _selector: source_pack)
    monkeypatch.setattr(cli, "_components", lambda: (paths, store, runtime, object()))
    monkeypatch.setattr(cli, "_launch_working", lambda **_kwargs: 0)

    args = cli._parser().parse_args(
        ["start", source_pack.id, "--editor", "terminal", "--skip-reading"]
    )
    assert cli._start(args) == 0

    (attempt,) = store.list_attempts()
    assert attempt.skip_reading is True
    frozen_root = paths.attempts / attempt.id / "pack"
    assert Path(attempt.pack_path) == frozen_root
    assert frozen_root.is_dir()
    assert not (frozen_root / "solutions").exists()
    assert load_pack(frozen_root).digest == attempt.pack_digest == source_pack.digest

    (source_root / "starter" / "q1.c").write_text("changed\n", encoding="utf-8")
    assert cli._attempt_pack(attempt).digest == attempt.pack_digest
    assert (frozen_root / "starter" / "q1.c").read_text(encoding="utf-8") != "changed\n"


def test_pack_default_exam_runs_entry_gate_then_reuses_reading_page_for_working(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source_root = make_pack(tmp_path / "source-pack")
    manifest = source_root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "reading_time_seconds = 0",
            'default_mode = "exam"\nreading_time_seconds = 600',
        ),
        encoding="utf-8",
    )
    source_pack = load_pack(source_root)
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    runtime = RuntimeStub()
    events: list[tuple[object, ...]] = []
    gate_courses: list[str] = []

    monkeypatch.setattr(cli.PackRepository, "get", lambda _self, _selector: source_pack)
    monkeypatch.setattr(cli, "_components", lambda: (paths, store, runtime, object()))

    def run_entry_gate(course: str) -> str:
        gate_courses.append(course)
        return "z1234567"

    monkeypatch.setattr(cli, "run_exam_entry_gate", run_entry_gate)

    def launch_reading_page(
        _paths: object, attempt: object, **kwargs: object
    ) -> SimpleNamespace:
        events.append(("page-ready", attempt.state))  # type: ignore[union-attr]
        callback = kwargs["ready_callback"]
        assert callable(callback)
        events.append(("page-open", attempt.state, kwargs.get("open_browser", True)))  # type: ignore[union-attr]
        callback()
        current = store.get_attempt(attempt.id)  # type: ignore[union-attr]
        events.append(("clock-started", current.state))
        return SimpleNamespace(url="http://127.0.0.1/reading/")

    monkeypatch.setattr(cli, "launch_companion", launch_reading_page)
    monkeypatch.setattr(
        cli,
        "_reading",
        lambda _pack, **_kwargs: events.append(("countdown",)),
    )

    def launch_working(**kwargs: object) -> int:
        attempt = kwargs["attempt"]
        events.append(
            (
                "working",
                attempt.state,  # type: ignore[union-attr]
                kwargs["open_companion_browser"],
            )
        )
        return 0

    monkeypatch.setattr(cli, "_launch_working", launch_working)

    args = cli._parser().parse_args(["start", source_pack.id, "--editor", "terminal"])
    assert cli._start(args) == 0
    assert gate_courses == ["COMP1511"]
    (attempt,) = store.list_attempts()
    assert attempt.mode is AttemptMode.EXAM
    assert attempt.timed is True
    assert attempt.candidate_id == "z1234567"
    assert events == [
        ("page-ready", AttemptState.CREATED),
        ("page-open", AttemptState.CREATED, True),
        ("clock-started", AttemptState.READING),
        ("countdown",),
        ("working", AttemptState.WORKING, False),
    ]


def test_resume_created_attempt_runs_reading_before_working(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source_root = make_pack(tmp_path / "source-pack")
    manifest = source_root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "reading_time_seconds = 0", "reading_time_seconds = 600"
        ),
        encoding="utf-8",
    )
    pack = load_pack(source_root)
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
        workspace_ref="resume-volume",
        image=pack.environment.image,
        editor="terminal",
        candidate_id="z1234567",
    )
    events: list[tuple[object, ...]] = []

    def launch_reading_page(
        _paths: object, pending: object, **kwargs: object
    ) -> SimpleNamespace:
        events.append(("page-open", pending.state))  # type: ignore[union-attr]
        callback = kwargs["ready_callback"]
        assert callable(callback)
        callback()
        current = store.get_attempt(pending.id)  # type: ignore[union-attr]
        events.append(("clock-started", current.state))
        return SimpleNamespace(url="http://127.0.0.1/reading/")

    monkeypatch.setattr(cli, "_components", lambda: (paths, store, RuntimeStub(), object()))
    monkeypatch.setattr(cli, "launch_companion", launch_reading_page)
    monkeypatch.setattr(
        cli,
        "_reading",
        lambda _pack, **_kwargs: events.append(("countdown",)),
    )

    def launch_working(**kwargs: object) -> int:
        current = kwargs["attempt"]
        events.append(
            (
                "working",
                current.state,  # type: ignore[union-attr]
                kwargs["open_companion_browser"],
            )
        )
        return 0

    monkeypatch.setattr(cli, "_launch_working", launch_working)

    assert cli._resume(cli._parser().parse_args(["resume", attempt.id])) == 0
    assert events == [
        ("page-open", AttemptState.CREATED),
        ("clock-started", AttemptState.READING),
        ("countdown",),
        ("working", AttemptState.WORKING, False),
    ]


def test_resume_created_attempt_preserves_skip_reading_choice(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source_root = make_pack(tmp_path / "source-pack")
    manifest = source_root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "reading_time_seconds = 0", "reading_time_seconds = 600"
        ),
        encoding="utf-8",
    )
    pack = load_pack(source_root)
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    attempt = store.create_attempt(
        pack_id=pack.id,
        pack_version=pack.version,
        pack_path=pack.root,
        pack_digest=pack.digest,
        course=pack.course,
        profile=pack.profile,
        mode=AttemptMode.PRACTICE,
        timed=False,
        created_at=datetime.now(UTC),
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="skip-reading-resume-volume",
        image=pack.environment.image,
        editor="terminal",
        skip_reading=True,
    )
    events: list[tuple[AttemptState, bool]] = []

    monkeypatch.setattr(cli, "_components", lambda: (paths, store, RuntimeStub(), object()))
    monkeypatch.setattr(
        cli,
        "_reading",
        lambda *_args, **_kwargs: pytest.fail("reading must remain skipped"),
    )
    monkeypatch.setattr(
        cli,
        "launch_companion",
        lambda *_args, **_kwargs: pytest.fail("the reading page must not launch"),
    )

    def launch_working(**kwargs: object) -> int:
        current = kwargs["attempt"]
        events.append(
            (
                current.state,  # type: ignore[union-attr]
                bool(kwargs["open_companion_browser"]),
            )
        )
        return 0

    monkeypatch.setattr(cli, "_launch_working", launch_working)

    assert cli._resume(cli._parser().parse_args(["resume", attempt.id])) == 0
    assert events == [(AttemptState.WORKING, True)]


def test_report_command_defaults_to_the_latest_attempt() -> None:
    args = cli._parser().parse_args(["report"])
    assert args.attempt_id is None


def test_report_command_rejects_created_attempt_without_exposing_paper(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    attempt = store.create_attempt(
        pack_id=pack.id,
        pack_version=pack.version,
        pack_path=pack.root,
        pack_digest=pack.digest,
        course=pack.course,
        profile=pack.profile,
        mode=AttemptMode.EXAM,
        timed=True,
        created_at=datetime.now(UTC),
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="created-report-volume",
        image=pack.environment.image,
        editor="terminal",
        candidate_id="z1234567",
    )
    monkeypatch.setattr(
        cli,
        "_components",
        lambda: (paths, store, RuntimeStub(), object()),
    )

    with pytest.raises(StateError, match="before reading time starts"):
        cli._report(cli._parser().parse_args(["report", attempt.id, "--json"]))

    assert capsys.readouterr().out == ""
    assert list(paths.reports.glob(f"{attempt.id}.*")) == []


def test_report_without_id_renders_the_newest_finished_attempt(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
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
        workspace_ref="report-volume",
        image=pack.environment.image,
        editor="terminal",
        candidate_id="z1234567",
    )
    attempt = store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=now,
        deadline_at=now + timedelta(hours=3),
    )
    store.transition(
        attempt.id,
        AttemptState.FINISHED,
        at=now,
        finish_reason="student",
    )
    monkeypatch.setattr(
        cli,
        "_components",
        lambda: (paths, store, RuntimeStub(), object()),
    )

    assert cli._report(cli._parser().parse_args(["report"])) == 0
    output = capsys.readouterr().out
    assert attempt.id in output
    assert (paths.reports / f"{attempt.id}.html").is_file()
    grade = store.get_grade(attempt.id)
    assert grade is not None
    assert grade["report_finalized_at"] is not None


def test_working_report_cannot_overwrite_a_concurrent_final_report(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    runtime = RuntimeStub()
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
        workspace_ref="report-race-volume",
        image=pack.environment.image,
        editor="terminal",
        candidate_id="z1234567",
    )
    attempt = store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=now,
        deadline_at=now + timedelta(hours=3),
    )
    monkeypatch.setattr(cli, "_components", lambda: (paths, store, runtime, object()))

    working_write_started = threading.Event()
    allow_working_write = threading.Event()
    finish_transitioned = threading.Event()
    original_write_reports = supervisor_module.write_reports
    original_transition = store.transition

    def delayed_write_reports(root: Path, attempt_id: str, document: object):
        assert isinstance(document, dict)
        if document["attempt"]["state"] == AttemptState.WORKING.value:
            working_write_started.set()
            assert allow_working_write.wait(timeout=5)
        return original_write_reports(root, attempt_id, document)

    def observed_transition(
        attempt_id: str,
        target: AttemptState,
        *,
        at: datetime,
        deadline_at: datetime | None = None,
        finish_reason: str | None = None,
    ):
        current = original_transition(
            attempt_id,
            target,
            at=at,
            deadline_at=deadline_at,
            finish_reason=finish_reason,
        )
        if target is AttemptState.FINISHED:
            finish_transitioned.set()
        return current

    monkeypatch.setattr(supervisor_module, "write_reports", delayed_write_reports)
    monkeypatch.setattr(store, "transition", observed_transition)
    failures: list[BaseException] = []

    def run_report() -> None:
        try:
            cli._report(cli._parser().parse_args(["report", attempt.id]))
        except BaseException as exc:  # pragma: no cover - asserted below
            failures.append(exc)

    service = AttemptService(
        store=store,
        runtime=runtime,  # type: ignore[arg-type]
        attempt=attempt,
        pack=pack,
        clock=FrozenClock(now),
    )

    def finish_attempt() -> None:
        try:
            service.finish()
        except BaseException as exc:  # pragma: no cover - asserted below
            failures.append(exc)

    report_thread = threading.Thread(target=run_report)
    finish_thread = threading.Thread(target=finish_attempt)
    report_thread.start()
    assert working_write_started.wait(timeout=5)
    finish_thread.start()
    assert finish_transitioned.wait(timeout=5)
    assert finish_thread.is_alive()
    allow_working_write.set()
    report_thread.join(timeout=5)
    finish_thread.join(timeout=5)

    assert not report_thread.is_alive()
    assert not finish_thread.is_alive()
    assert failures == []
    document = json.loads((paths.reports / f"{attempt.id}.json").read_text())
    assert document["attempt"]["state"] == AttemptState.FINISHED.value
    assert document["grade"] is not None
    grade = store.get_grade(attempt.id)
    assert grade is not None
    assert grade["report_finalized_at"] is not None


def test_working_launch_opens_isolated_code_and_companion(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
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
        editor="code",
        candidate_id="z1234567",
    )
    attempt = store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=now,
        deadline_at=now + timedelta(hours=3),
    )
    events: list[str] = []

    class LaunchRuntime:
        @staticmethod
        def start_container(*_args: object, **_kwargs: object) -> None:
            events.append("container")

    class LaunchVSCode:
        @staticmethod
        def offline_ready(_profile: str) -> tuple[bool, str]:
            return True, "ready"

        @staticmethod
        def attach(_attempt: object) -> None:
            events.append("code")

    monkeypatch.setattr(cli, "ensure_supervisor", lambda *_args: events.append("supervisor"))
    monkeypatch.setattr(
        cli,
        "launch_companion",
        lambda *_args, **_kwargs: (
            events.append("page") or SimpleNamespace(url="http://127.0.0.1/test/")
        ),
    )

    assert (
        cli._launch_working(
            attempt=attempt,
            pack=pack,
            paths=paths,
            store=store,
            runtime=LaunchRuntime(),  # type: ignore[arg-type]
            vscode=LaunchVSCode(),  # type: ignore[arg-type]
        )
        == 0
    )
    assert events == ["container", "supervisor", "page", "code"]


def test_working_launch_stops_expired_container_when_report_finalization_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    started = datetime.now(UTC) - timedelta(minutes=1)
    attempt = store.create_attempt(
        pack_id=pack.id,
        pack_version=pack.version,
        pack_path=pack.root,
        pack_digest=pack.digest,
        course=pack.course,
        profile=pack.profile,
        mode=AttemptMode.EXAM,
        timed=True,
        created_at=started,
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="expired-launch-volume",
        image=pack.environment.image,
        editor="terminal",
        candidate_id="z1234567",
    )
    attempt = store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=started,
        deadline_at=started + timedelta(seconds=1),
    )
    stopped: list[str] = []

    class ExpiredRuntime:
        @staticmethod
        def stop_container(current: object) -> None:
            stopped.append(current.id)  # type: ignore[union-attr]

    def fail_report(_service: object) -> object:
        raise RuntimeError("report failed")

    monkeypatch.setattr(cli.AttemptService, "finalize_report", fail_report)

    with pytest.raises(RuntimeError, match="report failed"):
        cli._launch_working(
            attempt=attempt,
            pack=pack,
            paths=paths,
            store=store,
            runtime=ExpiredRuntime(),  # type: ignore[arg-type]
            vscode=object(),  # type: ignore[arg-type]
        )
    assert store.get_attempt(attempt.id).state is AttemptState.EXPIRED
    assert stopped == [attempt.id]
