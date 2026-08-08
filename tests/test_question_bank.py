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
        _markdown(("## Background", "## Requirements", "## Examples", "## Implementation notes"))
        + f"\n\nSubmit `{filename}`.\n",
        encoding="utf-8",
    )
    (directory / "solution.md").write_text(
        _markdown(("## Approach", "## Correctness", "## Complexity", "## Common pitfalls"))
        + f"\n\nThe completed file is `{filename}`.\n",
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
    (directory / "question.json").write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")


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
    assert pack.title == "COMP1511 Generated Exam Paper"
    assert pack.paper_text().startswith("# COMP1511 Generated Exam Paper")
    assert pack.total_points == 100
    assert [question.id for question in pack.questions] == [f"q{index}" for index in range(1, 12)]
    assert all(question.prompt for question in pack.questions)
    assert (pack.root / "solutions" / "explanations" / "q1.md").is_file()
    for index, question in enumerate(pack.questions, start=1):
        student_filename = f"q{index}.c"
        original_filename = question.title.removeprefix("Original ").replace("-", "_") + ".c"
        assert question.starter_files == (f"starter/{student_filename}",)
        assert question.submission_files == (student_filename,)
        assert question.build_argv[-3:] == (student_filename, "-o", f"q{index}")
        assert all(
            test.argv[0] == f"./q{index}"
            for group in question.test_groups
            for test in group.tests
        )
        assert (pack.root / "starter" / student_filename).is_file()
        assert (pack.root / "solutions" / "reference" / student_filename).is_file()
        assert original_filename not in pack.question_prompt(question)
        assert student_filename in pack.question_prompt(question)
        explanation = (pack.root / "solutions" / "explanations" / f"q{index}.md").read_text(
            encoding="utf-8"
        )
        assert original_filename not in explanation
        assert student_filename in explanation


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
    first = pack.questions[0]
    original_filename = bank.questions[0].question.submission_files[0]
    assert first.starter_files == (f"starter/{original_filename}",)
    assert first.submission_files == (original_filename,)
    assert first.build_argv[-3:] == (original_filename, "-o", first.id)
    assert all(
        test.argv[0] == f"./{first.id}"
        for group in first.test_groups
        for test in group.tests
    )
    assert original_filename in pack.question_prompt(first)


@pytest.mark.parametrize("profile", ("comp1511", "comp1521"))
def test_bundled_generated_paper_uses_student_facing_filenames(
    tmp_path: Path, profile: str
) -> None:
    repository = Path(__file__).resolve().parents[1]
    bank = load_question_bank(repository / "question_bank" / profile)
    selection = select_exam(bank, seed=2026)
    pack = build_exam_pack(bank, destination=tmp_path / profile, seed=2026)

    for (slot, item), question in zip(selection, pack.questions, strict=True):
        original_filename = item.question.submission_files[0]
        suffix = "".join(Path(original_filename).suffixes)
        student_filename = f"{slot.id}{suffix}"
        assert question.starter_files == (f"starter/{student_filename}",)
        assert question.submission_files == (student_filename,)
        assert (pack.root / "starter" / student_filename).is_file()
        assert (pack.root / "solutions" / "reference" / student_filename).is_file()
        assert original_filename not in question.build_argv
        assert all(
            original_filename not in test.argv
            for group in question.test_groups
            for test in group.tests
        )
        assert original_filename not in pack.question_prompt(question)
        assert Path(original_filename).stem not in pack.question_prompt(question)
        explanation = (pack.root / "solutions" / "explanations" / f"{slot.id}.md").read_text(
            encoding="utf-8"
        )
        assert original_filename not in explanation
        assert Path(original_filename).stem not in explanation
        assert student_filename in pack.question_prompt(question)

    if profile == "comp1521":
        mips_question = pack.question("q3")
        assert mips_question.submission_files == ("q3.s",)
        assert all(
            test.argv[:2] == ("mipsy", "q3.s")
            for group in mips_question.test_groups
            for test in group.tests
        )


def test_rejects_prompt_without_required_sections(tmp_path: Path) -> None:
    root = _make_comp1511_bank(tmp_path / "bank")
    (root / "questions" / "list-a" / "prompt.md").write_text("# Too short\n", encoding="utf-8")
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


@pytest.mark.parametrize("profile", ("comp1511", "comp1521"))
def test_bundled_bank_has_150_questions_and_five_distinct_test_points(
    profile: str,
) -> None:
    repository = Path(__file__).resolve().parents[1]
    bank = load_question_bank(repository / "question_bank" / profile)
    expansion_prefixes = (
        (
            "c1511-array-",
            "c1511-list-",
            "c1511-text-",
            "c1511-logic-",
            "c1511-grid-",
            "c1511-record-",
            "c1511-system-",
        )
        if profile == "comp1511"
        else (
            "c1521-bits-",
            "c1521-mips-",
            "c1521-file-",
            "c1521-unicode-",
            "c1521-tree-",
            "c1521-thread-",
            "c1521-pipeline-",
        )
    )
    expansion_count = 0
    banned_prompt_phrases = (
        "metric named in the title",
        "metric in the title",
        "operation in the title",
        "rule named in the title",
        "public test",
        "(no command-line arguments)",
        "local CSEExamTTY simulator",
        "without relying on any UNSW assessment text",
        "public examples illustrate",
        "shell-free",
        "harness",
        "fixture-only",
    )
    assert len(bank.questions) == 150
    assert bank.minimum_test_points == 5
    assert set(bank.required_coverage_tags) == set(bank.allowed_tags)

    for item in bank.questions:
        tests = [test for group in item.question.test_groups for test in group.tests]
        assert len(tests) >= 5
        signatures = {
            (
                test.argv,
                test.stdin,
                tuple((fixture.source, fixture.path) for fixture in test.fixtures),
            )
            for test in tests
        }
        assert len(signatures) == len(tests), item.question.id
        solution = item.solution_text()
        assert "## Step-by-step" in solution
        assert "## Worked example" in solution
        assert item.question.prompt is not None
        prompt = (item.root / item.question.prompt).read_text(encoding="utf-8")
        assert "```text" in prompt
        assert not any(phrase in prompt for phrase in banned_prompt_phrases), item.question.id
        if item.question.id.startswith(expansion_prefixes):
            assert "## Task" in prompt
            assert "## Starter code" in prompt
            assert "## Submission" in prompt
            assert "## Exact rule" in solution
            expansion_count += 1

    assert expansion_count == 75


def test_concurrency_prompts_state_their_exact_output_grammar() -> None:
    repository = Path(__file__).resolve().parents[1]
    expected_rules = {
        "c1521-conc-006": "worker I lines=L bytes=B words=W",
        "c1521-conc-015": "INDEX value=V square=S cube=C",
        "c1521-conc-017": "INDEX square=S",
        "c1521-conc-020": "count=N even=E even_sum=ES odd=O odd_sum=OS min=MIN max=MAX",
    }
    for question_id, rule in expected_rules.items():
        prompt = (
            repository / "question_bank" / "comp1521" / "questions" / question_id / "prompt.md"
        ).read_text(encoding="utf-8")
        assert rule in prompt


@pytest.mark.parametrize("profile", ("comp1511", "comp1521"))
def test_random_papers_cover_every_tag_and_follow_difficulty_pattern(profile: str) -> None:
    repository = Path(__file__).resolve().parents[1]
    bank = load_question_bank(repository / "question_bank" / profile)
    papers: set[tuple[str, ...]] = set()

    for seed in range(250):
        selection = select_exam(bank, seed=seed)
        papers.add(tuple(item.question.id for _slot, item in selection))
        covered = {tag for _slot, item in selection for tag in item.question.tags}
        difficulties = tuple(item.question.difficulty for _slot, item in selection)
        assert covered.issuperset(bank.required_coverage_tags)
        assert difficulties == bank.difficulty_pattern
        assert difficulties == tuple(sorted(difficulties))
        assert len(set(difficulties)) >= 3

    assert len(papers) >= 200


def test_bank_can_require_a_minimum_number_of_test_points(tmp_path: Path) -> None:
    root = _make_comp1511_bank(tmp_path / "bank")
    manifest = root / "bank.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8") + "\nminimum_test_points = 5\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="at least 5 test points"):
        load_question_bank(root)
