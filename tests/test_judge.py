from __future__ import annotations

import sys
from pathlib import Path

from csetty.judge import _execute


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
