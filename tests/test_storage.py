from __future__ import annotations

import multiprocessing
import os
import subprocess
import sys
import threading
import time
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

import csetty.storage as storage_module
from csetty.errors import StateError, ValidationError
from csetty.models import AttemptMode, AttemptState, WorkspaceKind
from csetty.paths import AppPaths
from csetty.storage import Store, process_is_alive
from csetty.supervisor import _deadline_warning_thresholds


def _hold_report_lock(
    state_dir: str,
    attempt_id: str,
    ready_path: str,
    release_path: str,
) -> None:
    store = Store(AppPaths.discover(Path(state_dir)))
    with store.report_lock(attempt_id):
        Path(ready_path).touch()
        deadline = time.monotonic() + 10
        while not Path(release_path).exists():
            if time.monotonic() >= deadline:
                raise TimeoutError("parent did not release the report lock holder")
            time.sleep(0.02)


def make_store(tmp_path: Path) -> Store:
    return Store(AppPaths.discover(tmp_path / "state"))


def test_process_is_alive_dispatches_to_non_destructive_windows_probe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    checked: list[int] = []

    def probe(pid: int) -> bool:
        checked.append(pid)
        return False

    monkeypatch.setattr(storage_module, "_IS_WINDOWS", True)
    monkeypatch.setattr(storage_module, "_windows_process_is_alive", probe)

    assert not process_is_alive(43210)
    assert checked == [43210]


@pytest.mark.skipif(os.name != "nt", reason="requires the Windows process API")
def test_windows_process_liveness_probe_does_not_terminate_process() -> None:
    process = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        assert process_is_alive(process.pid)
        assert process.poll() is None
    finally:
        process.terminate()
        process.wait(timeout=5)

    assert not process_is_alive(process.pid)


def test_report_lock_serializes_another_process(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    attempt_id = "00000000-0000-4000-8000-000000000099"
    ready = tmp_path / "report-lock-ready"
    release = tmp_path / "report-lock-release"
    context = multiprocessing.get_context("spawn")
    holder = context.Process(
        target=_hold_report_lock,
        args=(str(store.paths.root), attempt_id, str(ready), str(release)),
    )
    holder.start()
    deadline = time.monotonic() + 10
    while not ready.exists():
        if not holder.is_alive():
            raise AssertionError(f"lock holder exited with {holder.exitcode}")
        if time.monotonic() >= deadline:
            raise AssertionError("lock holder did not become ready")
        time.sleep(0.02)

    started = time.monotonic()
    with (
        pytest.raises(StateError, match="report publication is still in progress"),
        store.report_lock(attempt_id, timeout=0.1),
    ):
        raise AssertionError("the held process lock must not be acquired")
    assert time.monotonic() - started < 2

    acquired = threading.Event()

    def acquire_after_holder() -> None:
        with store.report_lock(attempt_id):
            acquired.set()

    waiter = threading.Thread(target=acquire_after_holder)
    waiter.start()
    try:
        assert not acquired.wait(timeout=0.25)
        release.touch()
        assert acquired.wait(timeout=5)
    finally:
        release.touch(exist_ok=True)
        holder.join(timeout=5)
        if holder.is_alive():
            holder.terminate()
            holder.join(timeout=5)
        waiter.join(timeout=5)

    assert holder.exitcode == 0
    assert not waiter.is_alive()


def create_working_attempt(store: Store, now: datetime, *, deadline_seconds: int = 60):
    attempt = store.create_attempt(
        pack_id="pack",
        pack_version="1.0.0",
        pack_path=Path("/tmp/pack"),
        pack_digest="a" * 64,
        course="COMP1511",
        profile="comp1511",
        mode=AttemptMode.EXAM,
        timed=True,
        created_at=now,
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="csetty-test-volume",
        image="csetty/comp1511:dev",
        candidate_id="z1234567",
    )
    store.transition(attempt.id, AttemptState.READING, at=now)
    return store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=now,
        deadline_at=now + timedelta(seconds=deadline_seconds),
    )


def test_attempt_deadline_is_not_recalculated(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now)
    loaded = store.get_attempt(attempt.id)
    assert loaded.candidate_id == "z1234567"
    assert loaded.deadline_at == now + timedelta(seconds=60)
    assert (
        store.expire_if_due(attempt.id, now=now + timedelta(seconds=59)).state
        is AttemptState.WORKING
    )
    assert (
        store.expire_if_due(attempt.id, now=now + timedelta(seconds=60)).state
        is AttemptState.EXPIRED
    )


def test_attempt_provenance_round_trip(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = store.create_attempt(
        pack_id="pack",
        pack_version="1.0.0",
        pack_path=Path("/tmp/pack"),
        pack_digest="a" * 64,
        course="COMP1511",
        profile="comp1511",
        mode=AttemptMode.PRACTICE,
        timed=False,
        created_at=now,
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="csetty-provenance-volume",
        image="csetty/comp1511:dev",
        provenance={"image": {"id": "sha256:abc"}, "tools": {"dcc": {"version": "2.37"}}},
        skip_reading=True,
    )
    assert attempt.provenance["image"]["id"] == "sha256:abc"
    assert attempt.skip_reading is True
    assert store.get_attempt(attempt.id).provenance["tools"]["dcc"]["version"] == "2.37"
    assert store.get_attempt(attempt.id).skip_reading is True


def test_recording_a_new_grade_invalidates_report_finalization(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now)
    attempt = store.transition(
        attempt.id,
        AttemptState.FINISHED,
        at=now,
        finish_reason="student",
    )
    grade = {
        "score": {"earned": 0, "automatically_available": 0, "total": 0},
        "questions": [],
        "hurdles": [],
    }
    store.record_grade(
        attempt_id=attempt.id,
        created_at=now,
        earned="0",
        available="0",
        total="0",
        report=grade,
    )
    store.mark_report_finalized(attempt.id, at=now)
    finalized = store.get_grade(attempt.id)
    assert finalized is not None
    assert finalized["report_finalized_at"] is not None

    store.record_grade(
        attempt_id=attempt.id,
        created_at=now + timedelta(seconds=1),
        earned="0",
        available="0",
        total="0",
        report=grade,
    )
    invalidated = store.get_grade(attempt.id)
    assert invalidated is not None
    assert invalidated["report_finalized_at"] is None


def test_attempt_can_use_a_preallocated_canonical_id(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt_id = str(uuid.uuid4())
    attempt = store.create_attempt(
        pack_id="pack",
        pack_version="1.0.0",
        pack_path=Path("/tmp/pack"),
        pack_digest="a" * 64,
        course="COMP1511",
        profile="comp1511",
        mode=AttemptMode.PRACTICE,
        timed=False,
        created_at=now,
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="csetty-preallocated-volume",
        image="csetty/comp1511:dev",
        attempt_id=attempt_id,
    )
    assert attempt.id == attempt_id

    with pytest.raises(ValidationError, match="canonical UUID"):
        store.create_attempt(
            pack_id="pack",
            pack_version="1.0.0",
            pack_path=Path("/tmp/pack"),
            pack_digest="a" * 64,
            course="COMP1511",
            profile="comp1511",
            mode=AttemptMode.PRACTICE,
            timed=False,
            created_at=now,
            workspace_kind=WorkspaceKind.VOLUME,
            workspace_ref="csetty-invalid-id-volume",
            image="csetty/comp1511:dev",
            attempt_id="not-a-uuid",
        )


def test_submission_history_and_content_verification(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now)
    first = store.record_submission(
        attempt_id=attempt.id,
        question_id="q1",
        files={"q1.c": b"first\n"},
        created_at=now + timedelta(seconds=1),
    )
    second = store.record_submission(
        attempt_id=attempt.id,
        question_id="q1",
        files={"q1.c": b"second\n"},
        created_at=now + timedelta(seconds=2),
    )
    assert first["sequence"] == 1
    assert second["sequence"] == 2
    latest = store.latest_submission(attempt.id, "q1")
    assert latest is not None
    assert latest["sequence"] == 2
    materialized = tmp_path / "out"
    store.materialize_submission(latest, materialized)
    assert (materialized / "q1.c").read_bytes() == b"second\n"


def test_late_submission_is_rejected(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now, deadline_seconds=10)
    with pytest.raises(StateError, match="deadline"):
        store.record_submission(
            attempt_id=attempt.id,
            question_id="q1",
            files={"q1.c": b"late\n"},
            created_at=now + timedelta(seconds=10),
        )


def test_bridge_response_is_idempotent(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now)
    first = store.store_bridge_response(
        attempt_id=attempt.id,
        request_id="request-1",
        created_at=now,
        response={"exit_code": 0, "stdout": "first"},
    )
    second = store.store_bridge_response(
        attempt_id=attempt.id,
        request_id="request-1",
        created_at=now,
        response={"exit_code": 1, "stdout": "second"},
    )
    assert first == second == {"exit_code": 0, "stdout": "first"}


def test_deadline_warning_selects_nearest_due_threshold_and_is_once_only(
    tmp_path: Path,
) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now, deadline_seconds=4 * 60)
    thresholds = (3600, 1800, 900, 300)
    selected = store.pending_deadline_warning(
        attempt.id,
        remaining_seconds=240,
        thresholds=thresholds,
    )
    assert selected == 300
    store.record_deadline_warning(
        attempt.id,
        selected_threshold=selected,
        remaining_seconds=240,
        thresholds=thresholds,
        at=now,
    )
    assert (
        store.pending_deadline_warning(
            attempt.id,
            remaining_seconds=200,
            thresholds=thresholds,
        )
        is None
    )


def test_short_attempt_does_not_backfill_warnings_that_predate_its_start(
    tmp_path: Path,
) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now, deadline_seconds=305)
    thresholds = _deadline_warning_thresholds(attempt)

    assert thresholds == (300,)
    assert (
        store.pending_deadline_warning(
            attempt.id,
            remaining_seconds=304,
            thresholds=thresholds,
        )
        is None
    )
    assert (
        store.pending_deadline_warning(
            attempt.id,
            remaining_seconds=299,
            thresholds=thresholds,
        )
        == 300
    )


def test_deadline_warnings_are_selected_in_countdown_order(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now, deadline_seconds=2 * 60 * 60)
    thresholds = (3600, 1800, 900, 300)

    for remaining_seconds, expected in (
        (3599, 3600),
        (1799, 1800),
        (899, 900),
        (299, 300),
    ):
        selected = store.pending_deadline_warning(
            attempt.id,
            remaining_seconds=remaining_seconds,
            thresholds=thresholds,
        )
        assert selected == expected
        store.record_deadline_warning(
            attempt.id,
            selected_threshold=selected,
            remaining_seconds=remaining_seconds,
            thresholds=thresholds,
            at=now,
        )

    assert (
        store.pending_deadline_warning(
            attempt.id,
            remaining_seconds=0,
            thresholds=thresholds,
        )
        is None
    )
