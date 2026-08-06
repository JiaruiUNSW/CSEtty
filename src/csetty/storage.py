from __future__ import annotations

import errno
import importlib
import json
import os
import secrets
import sqlite3
import threading
import time
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager, suppress
from datetime import datetime
from pathlib import Path
from typing import Any

from .clock import from_iso, to_iso
from .errors import StateError, ValidationError
from .models import Attempt, AttemptMode, AttemptState, WorkspaceKind
from .paths import AppPaths
from .util import atomic_write, canonical_json, safe_relative_path, sha256_bytes

_TRANSITIONS: dict[AttemptState, set[AttemptState]] = {
    AttemptState.CREATED: {AttemptState.READING, AttemptState.WORKING, AttemptState.ABORTED},
    AttemptState.READING: {AttemptState.WORKING, AttemptState.EXPIRED, AttemptState.ABORTED},
    AttemptState.WORKING: {
        AttemptState.FINISHED,
        AttemptState.EXPIRED,
        AttemptState.ABORTED,
    },
    AttemptState.FINISHED: set(),
    AttemptState.EXPIRED: set(),
    AttemptState.ABORTED: set(),
}

_REPORT_THREAD_LOCKS: dict[Path, threading.Lock] = {}
_REPORT_THREAD_LOCKS_GUARD = threading.Lock()
_IS_WINDOWS = os.name == "nt"
_WINDOWS_SYNCHRONIZE = 0x00100000
_WINDOWS_WAIT_TIMEOUT = 0x00000102

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attempts (
    id TEXT PRIMARY KEY,
    pack_id TEXT NOT NULL,
    pack_version TEXT NOT NULL,
    pack_path TEXT NOT NULL,
    pack_digest TEXT NOT NULL,
    course TEXT NOT NULL,
    profile TEXT NOT NULL,
    candidate_id TEXT,
    mode TEXT NOT NULL,
    state TEXT NOT NULL,
    timed INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    reading_started_at TEXT,
    working_started_at TEXT,
    deadline_at TEXT,
    finished_at TEXT,
    finish_reason TEXT,
    workspace_kind TEXT NOT NULL,
    workspace_ref TEXT NOT NULL,
    image TEXT NOT NULL,
    provenance_json TEXT NOT NULL DEFAULT '{}',
    container_name TEXT NOT NULL UNIQUE,
    session_token TEXT NOT NULL,
    network TEXT NOT NULL DEFAULT 'none',
    editor TEXT NOT NULL DEFAULT 'code',
    skip_reading INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id TEXT NOT NULL REFERENCES attempts(id),
    question_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    manifest_digest TEXT NOT NULL,
    accepted INTEGER NOT NULL,
    UNIQUE(attempt_id, question_id, sequence)
);

CREATE TABLE IF NOT EXISTS submission_files (
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    path TEXT NOT NULL,
    object_digest TEXT NOT NULL,
    size INTEGER NOT NULL,
    PRIMARY KEY(submission_id, path)
);

CREATE TABLE IF NOT EXISTS test_runs (
    id TEXT PRIMARY KEY,
    attempt_id TEXT NOT NULL REFERENCES attempts(id),
    question_id TEXT NOT NULL,
    visibility TEXT NOT NULL,
    snapshot_digest TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    result_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS grades (
    attempt_id TEXT PRIMARY KEY REFERENCES attempts(id),
    created_at TEXT NOT NULL,
    earned TEXT NOT NULL,
    available TEXT NOT NULL,
    total TEXT NOT NULL,
    report_json TEXT NOT NULL,
    report_finalized_at TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id TEXT,
    created_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    detail_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supervisor_leases (
    attempt_id TEXT PRIMARY KEY REFERENCES attempts(id),
    pid INTEGER NOT NULL,
    heartbeat_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bridge_requests (
    attempt_id TEXT NOT NULL REFERENCES attempts(id),
    request_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    response_json TEXT NOT NULL,
    PRIMARY KEY(attempt_id, request_id)
);

CREATE TABLE IF NOT EXISTS deadline_warnings (
    attempt_id TEXT NOT NULL REFERENCES attempts(id),
    threshold_seconds INTEGER NOT NULL,
    recorded_at TEXT NOT NULL,
    broadcast INTEGER NOT NULL,
    PRIMARY KEY(attempt_id, threshold_seconds)
);

CREATE INDEX IF NOT EXISTS submissions_latest_idx
    ON submissions(attempt_id, question_id, accepted, sequence DESC);
CREATE INDEX IF NOT EXISTS events_attempt_idx ON events(attempt_id, id);
"""


class Store:
    def __init__(self, paths: AppPaths) -> None:
        self.paths = paths
        self.paths.ensure()
        self._migrate()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.paths.database, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    @contextmanager
    def transaction(self, *, immediate: bool = False) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @contextmanager
    def report_lock(
        self, attempt_id: str, *, timeout: float | None = None
    ) -> Iterator[None]:
        """Serialize report publication for one attempt across threads and processes."""
        if timeout is not None and timeout < 0:
            raise ValidationError("report lock timeout must be non-negative")
        try:
            parsed_id = uuid.UUID(attempt_id)
        except ValueError as exc:
            raise ValidationError("attempt id must be a canonical UUID") from exc
        if str(parsed_id) != attempt_id:
            raise ValidationError("attempt id must be a canonical UUID")

        path = self.paths.attempts / attempt_id / "report.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        resolved_path = path.resolve()
        with _REPORT_THREAD_LOCKS_GUARD:
            thread_lock = _REPORT_THREAD_LOCKS.setdefault(resolved_path, threading.Lock())

        deadline = None if timeout is None else time.monotonic() + timeout
        if deadline is None:
            thread_acquired = thread_lock.acquire()
        else:
            thread_acquired = thread_lock.acquire(
                timeout=max(0.0, deadline - time.monotonic())
            )
        if not thread_acquired:
            raise StateError("another report publication is still in progress")
        try:
            with path.open("a+b") as stream:
                stream.seek(0, os.SEEK_END)
                if stream.tell() == 0:
                    stream.write(b"\0")
                    stream.flush()
                stream.seek(0)
                if os.name == "nt":
                    lock_api: Any = importlib.import_module("msvcrt")

                    while True:
                        try:
                            lock_api.locking(stream.fileno(), lock_api.LK_NBLCK, 1)
                        except OSError as exc:
                            if exc.errno not in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                                raise
                            if deadline is not None and time.monotonic() >= deadline:
                                raise StateError(
                                    "another report publication is still in progress"
                                ) from exc
                            time.sleep(0.05)
                        else:
                            break
                    try:
                        yield
                    finally:
                        stream.seek(0)
                        with suppress(OSError):
                            lock_api.locking(stream.fileno(), lock_api.LK_UNLCK, 1)
                else:
                    lock_api = importlib.import_module("fcntl")
                    operation = lock_api.LOCK_EX
                    if deadline is not None:
                        operation |= lock_api.LOCK_NB
                    while True:
                        try:
                            lock_api.flock(stream.fileno(), operation)
                        except OSError as exc:
                            if exc.errno not in {
                                errno.EACCES,
                                errno.EAGAIN,
                                errno.EWOULDBLOCK,
                            }:
                                raise
                            if deadline is not None and time.monotonic() >= deadline:
                                raise StateError(
                                    "another report publication is still in progress"
                                ) from exc
                            time.sleep(0.05)
                        else:
                            break
                    try:
                        yield
                    finally:
                        with suppress(OSError):
                            lock_api.flock(stream.fileno(), lock_api.LOCK_UN)
        finally:
            thread_lock.release()

    def _migrate(self) -> None:
        with self._connect() as connection:
            connection.executescript(_SCHEMA)
            columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(attempts)").fetchall()
            }
            if "network" not in columns:
                connection.execute(
                    "ALTER TABLE attempts ADD COLUMN network TEXT NOT NULL DEFAULT 'none'"
                )
            if "editor" not in columns:
                connection.execute(
                    "ALTER TABLE attempts ADD COLUMN editor TEXT NOT NULL DEFAULT 'code'"
                )
            if "provenance_json" not in columns:
                connection.execute(
                    "ALTER TABLE attempts ADD COLUMN provenance_json TEXT NOT NULL DEFAULT '{}'"
                )
            if "candidate_id" not in columns:
                connection.execute("ALTER TABLE attempts ADD COLUMN candidate_id TEXT")
            if "skip_reading" not in columns:
                connection.execute(
                    "ALTER TABLE attempts ADD COLUMN skip_reading INTEGER NOT NULL DEFAULT 0"
                )
            grade_columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(grades)").fetchall()
            }
            if "report_finalized_at" not in grade_columns:
                connection.execute("ALTER TABLE grades ADD COLUMN report_finalized_at TEXT")
            connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES(1, ?)",
                (to_iso(datetime.now().astimezone()),),
            )
            connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES(2, ?)",
                (to_iso(datetime.now().astimezone()),),
            )
            connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES(3, ?)",
                (to_iso(datetime.now().astimezone()),),
            )
            connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES(4, ?)",
                (to_iso(datetime.now().astimezone()),),
            )
            connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES(5, ?)",
                (to_iso(datetime.now().astimezone()),),
            )

    def put_object(self, data: bytes) -> str:
        digest = sha256_bytes(data)
        target = self.paths.objects / digest[:2] / digest[2:]
        if not target.exists():
            atomic_write(target, data, mode=0o600)
        else:
            existing = target.read_bytes()
            if sha256_bytes(existing) != digest:
                raise ValidationError(f"content-addressed object is corrupt: {digest}")
        return digest

    def object_bytes(self, digest: str) -> bytes:
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ValidationError(f"invalid object digest: {digest!r}")
        path = self.paths.objects / digest[:2] / digest[2:]
        try:
            data = path.read_bytes()
        except FileNotFoundError as exc:
            raise ValidationError(f"submission object is missing: {digest}") from exc
        if sha256_bytes(data) != digest:
            raise ValidationError(f"submission object failed verification: {digest}")
        return data

    def create_attempt(
        self,
        *,
        pack_id: str,
        pack_version: str,
        pack_path: Path,
        pack_digest: str,
        course: str,
        profile: str,
        mode: AttemptMode,
        timed: bool,
        created_at: datetime,
        workspace_kind: WorkspaceKind,
        workspace_ref: str,
        image: str,
        provenance: Mapping[str, Any] | None = None,
        network: str = "none",
        editor: str = "code",
        candidate_id: str | None = None,
        skip_reading: bool = False,
        attempt_id: str | None = None,
    ) -> Attempt:
        if attempt_id is None:
            attempt_id = str(uuid.uuid4())
        else:
            try:
                parsed_attempt_id = uuid.UUID(attempt_id)
            except ValueError as exc:
                raise ValidationError("attempt_id must be a canonical UUID") from exc
            if str(parsed_attempt_id) != attempt_id:
                raise ValidationError("attempt_id must be a canonical UUID")
        container_name = f"csetty-{attempt_id[:12]}"
        session_token = secrets.token_urlsafe(32)
        with self.transaction(immediate=True) as connection:
            if workspace_kind is WorkspaceKind.BIND:
                conflict = connection.execute(
                    """
                    SELECT id FROM attempts
                    WHERE workspace_kind = ? AND workspace_ref = ?
                      AND state NOT IN ('FINISHED', 'EXPIRED', 'ABORTED')
                    """,
                    (workspace_kind.value, workspace_ref),
                ).fetchone()
                if conflict:
                    raise StateError(
                        f"workspace is already used by active attempt {conflict['id']}"
                    )
            connection.execute(
                """
                INSERT INTO attempts(
                    id, pack_id, pack_version, pack_path, pack_digest, course, profile,
                    candidate_id, mode, state, timed, created_at, workspace_kind, workspace_ref,
                    image, provenance_json, container_name, session_token, network, editor,
                    skip_reading
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    attempt_id,
                    pack_id,
                    pack_version,
                    str(pack_path),
                    pack_digest,
                    course,
                    profile,
                    candidate_id,
                    mode.value,
                    AttemptState.CREATED.value,
                    int(timed),
                    to_iso(created_at),
                    workspace_kind.value,
                    workspace_ref,
                    image,
                    canonical_json(dict(provenance or {})).decode(),
                    container_name,
                    session_token,
                    network,
                    editor,
                    int(skip_reading),
                ),
            )
            self._insert_event(
                connection,
                attempt_id=attempt_id,
                created_at=created_at,
                event_type="attempt.created",
                detail={
                    "mode": mode.value,
                    "pack_digest": pack_digest,
                    "candidate_id": candidate_id,
                    "skip_reading": skip_reading,
                },
            )
        return self.get_attempt(attempt_id)

    @staticmethod
    def _attempt_from_row(row: sqlite3.Row) -> Attempt:
        created_at = from_iso(row["created_at"])
        if created_at is None:
            raise ValidationError("attempt has invalid created_at")
        return Attempt(
            id=row["id"],
            pack_id=row["pack_id"],
            pack_version=row["pack_version"],
            pack_path=row["pack_path"],
            pack_digest=row["pack_digest"],
            course=row["course"],
            profile=row["profile"],
            mode=AttemptMode(row["mode"]),
            state=AttemptState(row["state"]),
            timed=bool(row["timed"]),
            created_at=created_at,
            reading_started_at=from_iso(row["reading_started_at"]),
            working_started_at=from_iso(row["working_started_at"]),
            deadline_at=from_iso(row["deadline_at"]),
            finished_at=from_iso(row["finished_at"]),
            finish_reason=row["finish_reason"],
            workspace_kind=WorkspaceKind(row["workspace_kind"]),
            workspace_ref=row["workspace_ref"],
            image=row["image"],
            provenance=json.loads(row["provenance_json"]),
            container_name=row["container_name"],
            session_token=row["session_token"],
            network=row["network"],
            editor=row["editor"],
            candidate_id=row["candidate_id"],
            skip_reading=bool(row["skip_reading"]),
        )

    def get_attempt(self, attempt_id: str) -> Attempt:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM attempts WHERE id = ?", (attempt_id,)
            ).fetchone()
        if row is None:
            raise ValidationError(f"attempt not found: {attempt_id}")
        return self._attempt_from_row(row)

    def resolve_attempt(self, selector: str | None) -> Attempt:
        if selector:
            with self._connect() as connection:
                rows = connection.execute(
                    "SELECT * FROM attempts WHERE id = ? OR id LIKE ? ORDER BY created_at DESC",
                    (selector, f"{selector}%"),
                ).fetchall()
            unique = {row["id"]: row for row in rows}
            if not unique:
                raise ValidationError(f"attempt not found: {selector}")
            if len(unique) > 1:
                raise ValidationError(f"attempt prefix is ambiguous: {selector}")
            return self._attempt_from_row(next(iter(unique.values())))
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM attempts
                WHERE state NOT IN ('FINISHED', 'EXPIRED', 'ABORTED')
                ORDER BY created_at DESC LIMIT 1
                """
            ).fetchone()
        if row is None:
            raise ValidationError("there is no active attempt")
        return self._attempt_from_row(row)

    def list_attempts(self) -> tuple[Attempt, ...]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM attempts ORDER BY created_at DESC").fetchall()
        return tuple(self._attempt_from_row(row) for row in rows)

    def transition(
        self,
        attempt_id: str,
        target: AttemptState,
        *,
        at: datetime,
        deadline_at: datetime | None = None,
        finish_reason: str | None = None,
    ) -> Attempt:
        with self.transaction(immediate=True) as connection:
            row = connection.execute(
                "SELECT * FROM attempts WHERE id = ?", (attempt_id,)
            ).fetchone()
            if row is None:
                raise ValidationError(f"attempt not found: {attempt_id}")
            current = AttemptState(row["state"])
            if target not in _TRANSITIONS[current]:
                raise StateError(
                    f"attempt cannot transition from {current.value} to {target.value}"
                )
            updates: dict[str, object] = {"state": target.value}
            if target is AttemptState.READING:
                updates["reading_started_at"] = to_iso(at)
            elif target is AttemptState.WORKING:
                updates["working_started_at"] = to_iso(at)
                updates["deadline_at"] = to_iso(deadline_at)
            elif target.terminal:
                updates["finished_at"] = to_iso(at)
                updates["finish_reason"] = finish_reason or target.value.lower()
            assignments = ", ".join(f"{column} = ?" for column in updates)
            connection.execute(
                f"UPDATE attempts SET {assignments} WHERE id = ?",  # noqa: S608 - trusted columns
                (*updates.values(), attempt_id),
            )
            self._insert_event(
                connection,
                attempt_id=attempt_id,
                created_at=at,
                event_type="attempt.transition",
                detail={"from": current.value, "to": target.value},
            )
        return self.get_attempt(attempt_id)

    def expire_if_due(self, attempt_id: str, *, now: datetime) -> Attempt:
        attempt = self.get_attempt(attempt_id)
        if (
            attempt.state in {AttemptState.READING, AttemptState.WORKING}
            and attempt.deadline_at is not None
            and now >= attempt.deadline_at
        ):
            return self.transition(
                attempt.id,
                AttemptState.EXPIRED,
                at=now,
                finish_reason="deadline",
            )
        return attempt

    def record_submission(
        self,
        *,
        attempt_id: str,
        question_id: str,
        files: Mapping[str, bytes],
        created_at: datetime,
    ) -> dict[str, Any]:
        if not files:
            raise ValidationError("a submission must contain at least one file")
        objects: list[dict[str, Any]] = []
        for file_path, content in sorted(files.items()):
            safe_relative_path(file_path, label="submission path")
            objects.append(
                {
                    "path": file_path,
                    "digest": self.put_object(content),
                    "size": len(content),
                }
            )
        manifest = {"schema": 1, "question": question_id, "files": objects}
        manifest_digest = self.put_object(canonical_json(manifest))

        with self.transaction(immediate=True) as connection:
            attempt_row = connection.execute(
                "SELECT state, deadline_at FROM attempts WHERE id = ?", (attempt_id,)
            ).fetchone()
            if attempt_row is None:
                raise ValidationError(f"attempt not found: {attempt_id}")
            state = AttemptState(attempt_row["state"])
            if state is not AttemptState.WORKING:
                raise StateError(f"submission is not allowed while attempt is {state.value}")
            deadline = from_iso(attempt_row["deadline_at"])
            if deadline is not None and created_at >= deadline:
                raise StateError("submission rejected: the deadline has passed")
            sequence_row = connection.execute(
                """
                SELECT COALESCE(MAX(sequence), 0) + 1 AS next_sequence
                FROM submissions WHERE attempt_id = ? AND question_id = ?
                """,
                (attempt_id, question_id),
            ).fetchone()
            if sequence_row is None or sequence_row["next_sequence"] is None:
                raise StateError("could not allocate a submission sequence")
            sequence = int(sequence_row["next_sequence"])
            cursor = connection.execute(
                """
                INSERT INTO submissions(
                    attempt_id, question_id, sequence, created_at, manifest_digest, accepted
                ) VALUES(?, ?, ?, ?, ?, 1)
                """,
                (attempt_id, question_id, sequence, to_iso(created_at), manifest_digest),
            )
            if cursor.lastrowid is None:
                raise StateError("submission record was not created")
            submission_id = int(cursor.lastrowid)
            connection.executemany(
                """
                INSERT INTO submission_files(submission_id, path, object_digest, size)
                VALUES(?, ?, ?, ?)
                """,
                [(submission_id, item["path"], item["digest"], item["size"]) for item in objects],
            )
            self._insert_event(
                connection,
                attempt_id=attempt_id,
                created_at=created_at,
                event_type="submission.accepted",
                detail={
                    "question": question_id,
                    "sequence": sequence,
                    "manifest_digest": manifest_digest,
                },
            )
        return {
            "id": submission_id,
            "attempt_id": attempt_id,
            "question_id": question_id,
            "sequence": sequence,
            "created_at": to_iso(created_at),
            "manifest_digest": manifest_digest,
            "files": objects,
        }

    def list_submissions(
        self, attempt_id: str, question_id: str | None = None
    ) -> list[dict[str, Any]]:
        query = "SELECT * FROM submissions WHERE attempt_id = ? AND accepted = 1"
        parameters: list[object] = [attempt_id]
        if question_id is not None:
            query += " AND question_id = ?"
            parameters.append(question_id)
        query += " ORDER BY question_id, sequence"
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
            result = []
            for row in rows:
                file_rows = connection.execute(
                    """
                    SELECT path, object_digest, size FROM submission_files
                    WHERE submission_id = ? ORDER BY path
                    """,
                    (row["id"],),
                ).fetchall()
                item = dict(row)
                item["files"] = [dict(file_row) for file_row in file_rows]
                result.append(item)
        return result

    def latest_submission(self, attempt_id: str, question_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM submissions
                WHERE attempt_id = ? AND question_id = ? AND accepted = 1
                ORDER BY sequence DESC LIMIT 1
                """,
                (attempt_id, question_id),
            ).fetchone()
            if row is None:
                return None
            files = connection.execute(
                """
                SELECT path, object_digest, size FROM submission_files
                WHERE submission_id = ? ORDER BY path
                """,
                (row["id"],),
            ).fetchall()
        result = dict(row)
        result["files"] = [dict(item) for item in files]
        return result

    def materialize_submission(self, submission: Mapping[str, Any], destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        for file_item in submission["files"]:
            relative = safe_relative_path(file_item["path"], label="submission path")
            target = destination.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(target, self.object_bytes(file_item["object_digest"]), mode=0o600)

    def record_test_run(
        self,
        *,
        attempt_id: str,
        question_id: str,
        visibility: str,
        snapshot_digest: str,
        status: str,
        created_at: datetime,
        result: Mapping[str, Any],
    ) -> str:
        run_id = str(uuid.uuid4())
        with self.transaction(immediate=True) as connection:
            connection.execute(
                """
                INSERT INTO test_runs(
                    id, attempt_id, question_id, visibility, snapshot_digest,
                    status, created_at, result_json
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    attempt_id,
                    question_id,
                    visibility,
                    snapshot_digest,
                    status,
                    to_iso(created_at),
                    canonical_json(result).decode(),
                ),
            )
        return run_id

    def has_test_run(self, attempt_id: str, question_id: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM test_runs WHERE attempt_id = ? AND question_id = ? LIMIT 1",
                (attempt_id, question_id),
            ).fetchone()
        return row is not None

    def record_grade(
        self,
        *,
        attempt_id: str,
        created_at: datetime,
        earned: str,
        available: str,
        total: str,
        report: Mapping[str, Any],
    ) -> None:
        with self.transaction(immediate=True) as connection:
            connection.execute(
                """
                INSERT INTO grades(attempt_id, created_at, earned, available, total, report_json)
                VALUES(?, ?, ?, ?, ?, ?)
                ON CONFLICT(attempt_id) DO UPDATE SET
                    created_at = excluded.created_at,
                    earned = excluded.earned,
                    available = excluded.available,
                    total = excluded.total,
                    report_json = excluded.report_json,
                    report_finalized_at = NULL
                """,
                (
                    attempt_id,
                    to_iso(created_at),
                    earned,
                    available,
                    total,
                    canonical_json(report).decode(),
                ),
            )

    def mark_report_finalized(self, attempt_id: str, *, at: datetime) -> None:
        """Publish report readiness only after both durable report files exist."""
        with self.transaction(immediate=True) as connection:
            cursor = connection.execute(
                "UPDATE grades SET report_finalized_at = ? WHERE attempt_id = ?",
                (to_iso(at), attempt_id),
            )
            if cursor.rowcount != 1:
                raise StateError("a report cannot be finalized before its grade is recorded")

    def invalidate_report_finalization(self, attempt_id: str) -> None:
        """Hide a previously published report while its files are being replaced."""
        with self.transaction(immediate=True) as connection:
            connection.execute(
                "UPDATE grades SET report_finalized_at = NULL WHERE attempt_id = ?",
                (attempt_id,),
            )

    def get_grade(self, attempt_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM grades WHERE attempt_id = ?", (attempt_id,)
            ).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["report"] = json.loads(result.pop("report_json"))
        return result

    def store_bridge_response(
        self,
        *,
        attempt_id: str,
        request_id: str,
        created_at: datetime,
        response: Mapping[str, Any],
    ) -> dict[str, Any]:
        encoded = canonical_json(response).decode()
        with self.transaction(immediate=True) as connection:
            existing = connection.execute(
                "SELECT response_json FROM bridge_requests WHERE attempt_id = ? AND request_id = ?",
                (attempt_id, request_id),
            ).fetchone()
            if existing is not None:
                decoded = json.loads(existing["response_json"])
                if not isinstance(decoded, dict) or not all(
                    isinstance(key, str) for key in decoded
                ):
                    raise ValidationError("stored bridge response is invalid")
                return {str(key): value for key, value in decoded.items()}
            connection.execute(
                """
                INSERT INTO bridge_requests(attempt_id, request_id, created_at, response_json)
                VALUES(?, ?, ?, ?)
                """,
                (attempt_id, request_id, to_iso(created_at), encoded),
            )
        return dict(response)

    def bridge_response(self, attempt_id: str, request_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT response_json FROM bridge_requests WHERE attempt_id = ? AND request_id = ?",
                (attempt_id, request_id),
            ).fetchone()
        if row is None:
            return None
        decoded = json.loads(row["response_json"])
        if not isinstance(decoded, dict) or not all(isinstance(key, str) for key in decoded):
            raise ValidationError("stored bridge response is invalid")
        return {str(key): value for key, value in decoded.items()}

    def pending_deadline_warning(
        self,
        attempt_id: str,
        *,
        remaining_seconds: int,
        thresholds: tuple[int, ...],
    ) -> int | None:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT threshold_seconds FROM deadline_warnings WHERE attempt_id = ?",
                (attempt_id,),
            ).fetchall()
        recorded = {int(row["threshold_seconds"]) for row in rows}
        due = [
            threshold
            for threshold in thresholds
            if remaining_seconds <= threshold and threshold not in recorded
        ]
        return min(due) if due else None

    def record_deadline_warning(
        self,
        attempt_id: str,
        *,
        selected_threshold: int,
        remaining_seconds: int,
        thresholds: tuple[int, ...],
        at: datetime,
    ) -> None:
        due = [threshold for threshold in thresholds if remaining_seconds <= threshold]
        with self.transaction(immediate=True) as connection:
            connection.executemany(
                """
                INSERT OR IGNORE INTO deadline_warnings(
                    attempt_id, threshold_seconds, recorded_at, broadcast
                ) VALUES(?, ?, ?, ?)
                """,
                [
                    (
                        attempt_id,
                        threshold,
                        to_iso(at),
                        int(threshold == selected_threshold),
                    )
                    for threshold in due
                ],
            )
            self._insert_event(
                connection,
                attempt_id=attempt_id,
                created_at=at,
                event_type="deadline.warning",
                detail={
                    "threshold_seconds": selected_threshold,
                    "remaining_seconds": remaining_seconds,
                },
            )

    def update_lease(self, *, attempt_id: str, pid: int, at: datetime) -> None:
        with self.transaction(immediate=True) as connection:
            connection.execute(
                """
                INSERT INTO supervisor_leases(attempt_id, pid, heartbeat_at)
                VALUES(?, ?, ?)
                ON CONFLICT(attempt_id) DO UPDATE SET
                    pid = excluded.pid, heartbeat_at = excluded.heartbeat_at
                """,
                (attempt_id, pid, to_iso(at)),
            )

    def remove_lease(self, attempt_id: str, *, pid: int | None = None) -> None:
        with self.transaction(immediate=True) as connection:
            if pid is None:
                connection.execute(
                    "DELETE FROM supervisor_leases WHERE attempt_id = ?", (attempt_id,)
                )
            else:
                connection.execute(
                    "DELETE FROM supervisor_leases WHERE attempt_id = ? AND pid = ?",
                    (attempt_id, pid),
                )

    def lease(self, attempt_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM supervisor_leases WHERE attempt_id = ?", (attempt_id,)
            ).fetchone()
        return None if row is None else dict(row)

    @staticmethod
    def _insert_event(
        connection: sqlite3.Connection,
        *,
        attempt_id: str | None,
        created_at: datetime,
        event_type: str,
        detail: Mapping[str, Any],
    ) -> None:
        connection.execute(
            """
            INSERT INTO events(attempt_id, created_at, event_type, detail_json)
            VALUES(?, ?, ?, ?)
            """,
            (attempt_id, to_iso(created_at), event_type, canonical_json(detail).decode()),
        )

    def close(self) -> None:
        """Compatibility hook; Store uses short-lived connections."""


def _windows_process_is_alive(pid: int) -> bool:
    """Check a Windows process without signalling or terminating it."""

    import ctypes
    from ctypes import wintypes

    win_dll = getattr(ctypes, "WinDLL", None)
    if win_dll is None:
        return False
    kernel32 = win_dll("kernel32", use_last_error=True)
    open_process = kernel32.OpenProcess
    open_process.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    open_process.restype = wintypes.HANDLE
    wait_for_single_object = kernel32.WaitForSingleObject
    wait_for_single_object.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    wait_for_single_object.restype = wintypes.DWORD
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    handle = open_process(_WINDOWS_SYNCHRONIZE, False, pid)
    if not handle:
        return False
    try:
        status = int(wait_for_single_object(handle, 0))
        return status == _WINDOWS_WAIT_TIMEOUT
    finally:
        close_handle(handle)


def process_is_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if _IS_WINDOWS:
        return _windows_process_is_alive(pid)
    try:
        os.kill(pid, 0)
    except (OSError, ProcessLookupError):
        return False
    return True
