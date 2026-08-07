from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class AttemptMode(StrEnum):
    PRACTICE = "practice"
    EXAM = "exam"


class AttemptState(StrEnum):
    CREATED = "CREATED"
    READING = "READING"
    WORKING = "WORKING"
    FINISHED = "FINISHED"
    EXPIRED = "EXPIRED"
    ABORTED = "ABORTED"

    @property
    def terminal(self) -> bool:
        return self in {self.FINISHED, self.EXPIRED, self.ABORTED}


class WorkspaceKind(StrEnum):
    VOLUME = "volume"
    BIND = "bind"


class TestVisibility(StrEnum):
    PUBLIC = "public"
    AFTER_FINISH = "after_finish"


class ResultClass(StrEnum):
    PASS = "PASS"
    COMPILE_ERROR = "COMPILE_ERROR"
    WRONG_OUTPUT = "WRONG_OUTPUT"
    WRONG_EXIT_STATUS = "WRONG_EXIT_STATUS"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    TIMEOUT = "TIMEOUT"
    OUTPUT_LIMIT = "OUTPUT_LIMIT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


@dataclass(frozen=True)
class Attempt:
    id: str
    pack_id: str
    pack_version: str
    pack_path: str
    pack_digest: str
    course: str
    profile: str
    mode: AttemptMode
    state: AttemptState
    timed: bool
    created_at: datetime
    reading_started_at: datetime | None
    working_started_at: datetime | None
    deadline_at: datetime | None
    finished_at: datetime | None
    finish_reason: str | None
    workspace_kind: WorkspaceKind
    workspace_ref: str
    image: str
    provenance: Mapping[str, Any]
    container_name: str
    session_token: str
    network: str
    editor: str
    candidate_id: str | None = None
    skip_reading: bool = False


@dataclass(frozen=True)
class TestOutcome:
    test_id: str
    result: ResultClass
    duration_ms: int
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    detail: str = ""
