from __future__ import annotations

import json
import os
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

from test_storage import create_working_attempt, make_store

from csetty.bridge import BridgeServer
from csetty.clock import FrozenClock


def _request(attempt, request_id: str, **overrides):
    payload = {
        "protocol": 1,
        "request_id": request_id,
        "attempt_id": attempt.id,
        "session_token": attempt.session_token,
        "operation": "status",
        "arguments": {},
    }
    payload.update(overrides)
    return payload


def test_bridge_replays_same_uuid_without_reexecuting(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now)
    root = tmp_path / "bridge"
    bridge = BridgeServer(root=root, attempt=attempt, store=store, clock=FrozenClock(now))
    request_id = str(uuid.uuid4())
    request_path = root / "requests" / f"{request_id}.json"
    request_path.write_text(json.dumps(_request(attempt, request_id)), encoding="utf-8")
    calls = 0

    def handler(_payload):
        nonlocal calls
        calls += 1
        return {"exit_code": 0, "stdout": "first", "stderr": ""}

    assert bridge.process_once(handler) == 1
    request_path.write_text(json.dumps(_request(attempt, request_id)), encoding="utf-8")
    assert bridge.process_once(handler) == 1
    response = json.loads((root / "responses" / f"{request_id}.json").read_text())
    assert response["stdout"] == "first"
    assert calls == 1


def test_bridge_rejects_future_request_and_wrong_token(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    now = datetime(2026, 8, 5, tzinfo=UTC)
    attempt = create_working_attempt(store, now)
    root = tmp_path / "bridge"
    bridge = BridgeServer(root=root, attempt=attempt, store=store, clock=FrozenClock(now))

    future_id = str(uuid.uuid4())
    future = root / "requests" / f"{future_id}.json"
    future.write_text(json.dumps(_request(attempt, future_id)), encoding="utf-8")
    future_time = time.time() + 60
    os.utime(future, (future_time, future_time))

    token_id = str(uuid.uuid4())
    wrong_token = root / "requests" / f"{token_id}.json"
    wrong_token.write_text(
        json.dumps(_request(attempt, token_id, session_token="wrong")), encoding="utf-8"
    )
    bridge.process_once(lambda _payload: {"exit_code": 0})
    future_response = json.loads((root / "responses" / f"{future_id}.json").read_text())
    token_response = json.loads((root / "responses" / f"{token_id}.json").read_text())
    assert future_response["exit_code"] != 0
    assert "stale" in future_response["stderr"]
    assert token_response["exit_code"] != 0
    assert "token" in token_response["stderr"]
