from __future__ import annotations

import json
from pathlib import Path

import pytest

from csetty.errors import ValidationError
from csetty.question_bank import (
    build_exam_pack,
    build_verification_pack,
    load_question_bank,
    select_exam,
)


def _markdown(headings: tuple[str, ...]) -> str:
    return "# Original task\n\n" + "\n\n".join(
        f"{heading}\n\nThis section contains original explanatory material, constraints, and "
        "enough detail for a student to use the document independently."
        for heading in headings
    )


def _add_question(root: Path, *, question_id: str, slot: str, points: int) -> None:
    directory = root / "questions" / question_id
    (directory / "starter").mkdir(parents=True)
    (directory / "reference").mkdir()
    filename = f"{question_id.replace('-', '_')}.c"
    source = "int main(void) { return 0; }\n"
    (directory / "starter" / filename).write_text(source, encoding="utf-8")
    (directory / "reference" / filename).write_text(source, encoding="utf-8")
    (directory / "prompt.md").write_text(
        _markdown(("## Background", "## Requirements", "## Examples", "## Implementation notes")),
        encoding="utf-8",
    )
    (directory / "solution.md").write_text(
        _markdown(("## Approach", "## Correctness", "## Complexity", "## Common pitfalls")),
        encoding="utf-8",
    )
    public_points = points // 2
    raw = {
        "schema_version": 1,
        "id": question_id,
        "title": f"Original {question_id}",
        "kind": "c_program",
        "difficulty": 2,
        "track": "normal",
        "tags": ["testing"],
        "weeks": [4],
        "slots": [slot],
        "estimated_minutes": 15,
        "points": points,
        "pass_points": public_points,
        "prompt": "prompt.md",
        "solution": "solution.md",
        "starter_files": [f"starter/{filename}"],
        "submission_files": [filename],
        "build": {"argv": ["dcc", "-Werror", filename, "-o", question_id]},
        "test_groups": [
            {
                "id": "public",
                "visibility": "public",
                "points": public_points,
                "tests": [
                    {
                        "id": "basic",
                        "argv": [f"./{question_id}"],
                        "expected_stdout": "",
                        "expected_stderr": "",
                        "expected_exit": 0,
                    }
                ],
            },
            {
                "id": "marking",
                "visibility": "after_finish",
                "points": points - public_points,
                "tests": [
                    {
                        "id": "boundary",
                        "argv": [f"./{question_id}"],
                        "expected_stdout": "",
                        "expected_stderr": "",
                        "expected_exit": 0,
                    }
                ],
            },
        ],
    }
    (directory / "question.json").write_text(
        json.dumps(raw, indent=2) + "\n", encoding="utf-8"
    )


def _make_comp1511_bank(root: Path) -> Path:
    root.mkdir()
    (root / "bank.toml").write_text(
        """
schema_version = 1
id = "test-bank"
title = "Test bank"
course = "COMP1511"
profile = "comp1511"
author = "Tests"
license = "CC BY-NC-ND 4.0"
allowed_slots = ["list_hurdle", "array_hurdle", "short", "medium", "whole_program"]
allowed_tags = ["testing"]
""",
        encoding="utf-8",
    )
    specifications = (
        ("list-a", "list_hurdle", 12),
        ("list-b", "list_hurdle", 12),
        ("array-a", "array_hurdle", 12),
        ("array-b", "array_hurdle", 12),
        ("short-a", "short", 5),
        ("short-b", "short", 5),
        ("short-c", "short", 5),
        ("short-d", "short", 5),
        ("medium-a", "medium", 11),
        ("medium-b", "medium", 11),
        ("whole-a", "whole_program", 10),
    )
    for question_id, slot, points in specifications:
        _add_question(root, question_id=question_id, slot=slot, points=points)
    return root


def test_load_question_bank_and_stats(tmp_path: Path) -> None:
    bank = load_question_bank(_make_comp1511_bank(tmp_path / "bank"))
    assert len(bank.questions) == 11
    assert bank.stats()["by_slot"]["short"] == 4
    assert bank.stats()["by_difficulty"] == {"2": 11}


def test_build_deterministic_exam_pack(tmp_path: Path) -> None:
    bank = load_question_bank(_make_comp1511_bank(tmp_path / "bank"))
    pack = build_exam_pack(bank, destination=tmp_path / "pack", seed=1511)
    assert pack.total_points == 100
    assert [question.id for question in pack.questions] == [f"q{index}" for index in range(1, 12)]
    assert all(question.prompt for question in pack.questions)
    assert (pack.root / "solutions" / "explanations" / "q1.md").is_file()


def test_build_verification_pack_contains_every_bank_question(tmp_path: Path) -> None:
    bank = load_question_bank(_make_comp1511_bank(tmp_path / "bank"))
    pack = build_verification_pack(bank, destination=tmp_path / "verification")
    assert [question.id for question in pack.questions] == [
        item.question.id for item in bank.questions
    ]
    assert len(pack.questions) == 11
    assert (
        pack.root / "solutions" / "reference" / bank.questions[0].question.submission_files[0]
    ).is_file()


def test_rejects_prompt_without_required_sections(tmp_path: Path) -> None:
    root = _make_comp1511_bank(tmp_path / "bank")
    (root / "questions" / "list-a" / "prompt.md").write_text(
        "# Too short\n", encoding="utf-8"
    )
    with pytest.raises(ValidationError, match="too short|missing headings"):
        load_question_bank(root)


def test_bundled_comp1521_blueprint_guarantees_foundation_mix() -> None:
    repository = Path(__file__).resolve().parents[1]
    bank = load_question_bank(repository / "question_bank" / "comp1521")
    for seed in range(20):
        selected = select_exam(bank, seed=seed)
        by_position = {slot.id: set(item.question.tags) for slot, item in selected}
        assert "file-io" in by_position["q1"]
        assert by_position["q2"] & {"bitwise", "integer-representation"}
        assert by_position["q3"] & {
            "mips-basics",
            "mips-control",
            "mips-data",
            "mips-functions",
        }


def test_short_profile_selector_loads_bundled_bank() -> None:
    assert load_question_bank("comp1511").id == "comp1511-original-bank"
    assert load_question_bank("comp1521").id == "comp1521-original-bank"
