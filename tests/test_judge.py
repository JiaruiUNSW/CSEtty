from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import csetty.judge as judge_module
from csetty.judge import _execute


class _FakeProcess:
    def __init__(self, return_code: int | None) -> None:
        self.pid = 123
        self.return_code = return_code
        self.kill_calls = 0

    def poll(self) -> int | None:
        return self.return_code

    def kill(self) -> None:
        self.kill_calls += 1


def test_kill_process_group_falls_back_after_permission_race(
    monkeypatch: Any,
) -> None:
    process = _FakeProcess(return_code=None)

    def deny_group_kill(pid: int, sig: int) -> None:
        raise PermissionError

    monkeypatch.setattr(judge_module.sys, "platform", "darwin")
    monkeypatch.setattr(judge_module.os, "killpg", deny_group_kill, raising=False)

    judge_module._kill_process_group(process)  # type: ignore[arg-type]

    assert process.kill_calls == 1


def test_kill_process_group_ignores_permission_race_after_exit(
    monkeypatch: Any,
) -> None:
    process = _FakeProcess(return_code=0)

    def deny_group_kill(pid: int, sig: int) -> None:
        raise PermissionError

    monkeypatch.setattr(judge_module.sys, "platform", "darwin")
    monkeypatch.setattr(judge_module.os, "killpg", deny_group_kill, raising=False)

    judge_module._kill_process_group(process)  # type: ignore[arg-type]

    assert process.kill_calls == 0


def test_output_limit_does_not_limit_build_artifacts(tmp_path: Path) -> None:
    execution = _execute(
        [
            sys.executable,
            "-c",
            "from pathlib import Path; Path('artifact').write_bytes(b'x' * 4096)",
        ],
        cwd=tmp_path,
        stdin="",
        timeout_ms=1000,
        output_limit=64,
    )
    assert execution["exit_code"] == 0
    assert execution["output_limited"] is False
    assert (tmp_path / "artifact").stat().st_size == 4096


def test_output_flood_and_timeout_are_classified(tmp_path: Path) -> None:
    flooded = _execute(
        [sys.executable, "-c", "import sys; sys.stdout.write('x' * 1000000)"],
        cwd=tmp_path,
        stdin="",
        timeout_ms=2000,
        output_limit=1024,
    )
    assert flooded["output_limited"] is True
    assert len(flooded["stdout"].encode()) <= 1024

    timed = _execute(
        [sys.executable, "-c", "import time; time.sleep(2)"],
        cwd=tmp_path,
        stdin="",
        timeout_ms=50,
        output_limit=1024,
    )
    assert timed["timed_out"] is True
