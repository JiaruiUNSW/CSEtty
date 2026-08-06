from __future__ import annotations

import json
import os
import time
import uuid
from collections import deque
from collections.abc import Callable, Mapping
from contextlib import suppress
from pathlib import Path
from typing import Any

from .clock import Clock
from .errors import CSETTYError, ValidationError
from .models import Attempt
from .storage import Store
from .util import atomic_write, canonical_json

_ALLOWED_OPERATIONS = {
    "autotest",
    "check",
    "fetch",
    "finish",
    "questions",
    "status",
    "submission",
    "submissions",
    "submit",
}
_MAX_REQUEST_BYTES = 64 * 1024
_RATE_WINDOW_SECONDS = 2.0
_RATE_MAX_REQUESTS = 30


class BridgeServer:
    def __init__(self, *, root: Path, attempt: Attempt, store: Store, clock: Clock) -> None:
        self.root = root
        self.attempt = attempt
        self.store = store
        self.clock = clock
        self.requests = root / "requests"
        self.responses = root / "responses"
        self.processed = root / "processed"
        self._request_times: deque[float] = deque()
        for directory in (self.requests, self.responses, self.processed):
            directory.mkdir(parents=True, exist_ok=True)

    def process_once(self, handler: Callable[[Mapping[str, Any]], Mapping[str, Any]]) -> int:
        processed_count = 0

        def modified(path: Path) -> float:
            try:
                return path.lstat().st_mtime
            except OSError:
                return 0.0

        for request_path in sorted(self.requests.glob("*.json"), key=modified):
            processed_count += 1
            response = self._process(request_path, handler)
            request_id = request_path.stem
            response_path = self.responses / f"{request_id}.json"
            with suppress(OSError):
                atomic_write(response_path, canonical_json(response), mode=0o644)
                # A container process can deny its own response by pre-creating a directory,
                # but must not be able to terminate the host supervisor.
            with suppress(FileNotFoundError):
                os.replace(request_path, self.processed / request_path.name)
        return processed_count

    def _process(
        self,
        request_path: Path,
        handler: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    ) -> dict[str, Any]:
        try:
            if request_path.is_symlink() or not request_path.is_file():
                raise ValidationError("bridge request is not a regular file")
            if request_path.stat().st_size > _MAX_REQUEST_BYTES:
                raise ValidationError("bridge request exceeds 64 KiB")
            age = time.time() - request_path.lstat().st_mtime
            if age > 300 or age < -5:
                raise ValidationError("bridge request is stale")
            request = json.loads(request_path.read_text(encoding="utf-8"))
            if not isinstance(request, dict):
                raise ValidationError("bridge request must be a JSON object")
            self._validate(request, request_path.stem)
            request_id = str(request["request_id"])
            existing = self.store.bridge_response(self.attempt.id, request_id)
            if existing is not None:
                return existing
            now = time.monotonic()
            while self._request_times and now - self._request_times[0] > _RATE_WINDOW_SECONDS:
                self._request_times.popleft()
            if len(self._request_times) >= _RATE_MAX_REQUESTS:
                raise ValidationError("bridge request rate limit exceeded")
            self._request_times.append(now)
            response = dict(handler(request))
            response.setdefault("exit_code", 0)
            response.setdefault("stdout", "")
            response.setdefault("stderr", "")
            response["request_id"] = request_id
            return self.store.store_bridge_response(
                attempt_id=self.attempt.id,
                request_id=request_id,
                created_at=self.clock.now(),
                response=response,
            )
        except CSETTYError as exc:
            return {
                "request_id": request_path.stem,
                "exit_code": exc.exit_code,
                "stdout": "",
                "stderr": exc.message + "\n",
            }
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            return {
                "request_id": request_path.stem,
                "exit_code": 5,
                "stdout": "",
                "stderr": f"invalid bridge request: {exc}\n",
            }

    def _validate(self, request: Mapping[str, Any], filename_id: str) -> None:
        if request.get("protocol") != 1:
            raise ValidationError("unsupported bridge protocol")
        request_id = request.get("request_id")
        try:
            parsed_id = uuid.UUID(str(request_id))
        except (ValueError, TypeError) as exc:
            raise ValidationError("request_id must be a UUID") from exc
        if str(parsed_id) != filename_id:
            raise ValidationError("request filename does not match request_id")
        if request.get("attempt_id") != self.attempt.id:
            raise ValidationError("bridge request targets the wrong attempt")
        if request.get("session_token") != self.attempt.session_token:
            raise ValidationError("bridge request session token is invalid")
        operation = request.get("operation")
        if operation not in _ALLOWED_OPERATIONS:
            raise ValidationError(f"bridge operation is not allowed: {operation!r}")
        arguments = request.get("arguments", {})
        if not isinstance(arguments, dict):
            raise ValidationError("bridge arguments must be an object")
