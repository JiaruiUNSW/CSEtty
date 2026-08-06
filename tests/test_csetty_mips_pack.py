from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
from csetty_mips import SourceUnit, assemble
from csetty_mips.machine import Machine

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs" / "comp1521-original-a"


def _mips_cases() -> list[tuple[str, str, str]]:
    manifest = tomllib.loads((PACK / "pack.toml").read_text(encoding="utf-8"))
    result: list[tuple[str, str, str]] = []
    for question in manifest["questions"]:
        if question["kind"] != "mips_program":
            continue
        for group in question["test_groups"]:
            for test in group["tests"]:
                result.append((question["id"], test.get("stdin", ""), test["expected_stdout"]))
    return result


@pytest.mark.parametrize(("question", "stdin", "expected"), _mips_cases())
def test_current_pack_reference_programs(question: str, stdin: str, expected: str) -> None:
    path = PACK / "solutions" / "reference" / f"{question}.s"
    program = assemble([SourceUnit(str(path), path.read_text(encoding="utf-8"))])
    machine = Machine(program, input_data=stdin.encode())
    assert machine.run() == 0
    assert machine.io.output.decode() == expected
