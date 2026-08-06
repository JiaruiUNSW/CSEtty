from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from csetty.errors import StateError, ValidationError
from csetty.models import AttemptMode, AttemptState, WorkspaceKind
from csetty.paths import AppPaths
from csetty.storage import Store
from csetty.supervisor import _deadline_warning_thresholds


def make_store(tmp_path: Path) -> Store:
    return Store(AppPaths.discover(tmp_path / "state"))


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
    )
    assert attempt.provenance["image"]["id"] == "sha256:abc"
    assert store.get_attempt(attempt.id).provenance["tools"]["dcc"]["version"] == "2.37"


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
