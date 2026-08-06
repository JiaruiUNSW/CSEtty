from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from csetty_mips import SourceUnit, assemble
from csetty_mips.machine import Machine

ROOT = Path(__file__).resolve().parents[1]
QUESTION_ROOT = ROOT / "question_bank" / "comp1521" / "questions"


def _reference_cases() -> list[tuple[str, Path, dict[str, Any]]]:
    cases: list[tuple[str, Path, dict[str, Any]]] = []
    for manifest in sorted(QUESTION_ROOT.glob("*/question.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data["kind"] != "mips_program":
            continue
        submission = data["submission_files"][0]
        reference = manifest.parent / "reference" / submission
        for group in data["test_groups"]:
            for test in group["tests"]:
                case_id = f"{data['id']}:{group['id']}:{test['id']}"
                cases.append((case_id, reference, test))
    return cases


@pytest.mark.parametrize(
    ("case_id", "reference", "test"),
    _reference_cases(),
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_all_original_question_bank_mips_references(
    case_id: str,
    reference: Path,
    test: dict[str, Any],
) -> None:
    del case_id
    program = assemble([SourceUnit(str(reference), reference.read_text(encoding="utf-8"))])
    runtime_argv = tuple(test["argv"][2:])
    machine = Machine(
        program,
        argv=runtime_argv,
        input_data=test["stdin"].encode(),
    )
    assert machine.run() == test["expected_exit"]
    assert machine.io.output.decode() == test["expected_stdout"]
