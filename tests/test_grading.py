from __future__ import annotations

from pathlib import Path

import pytest
from test_pack import make_pack

from csetty.grading import calculate_grade
from csetty.models import ResultClass
from csetty.pack import load_pack


def test_weighted_groups_and_hurdle(tmp_path: Path) -> None:
    root = make_pack(
        tmp_path / "pack",
        extra="""

[[hurdles]]
id = "core"
label = "Core hurdle"
question_ids = ["q1"]
min_passed_questions = 1
""",
    )
    pack = load_pack(root)
    grade = calculate_grade(
        pack,
        {
            "q1": {
                "public": [ResultClass.PASS],
                "marking": [ResultClass.WRONG_OUTPUT],
            }
        },
    )
    assert grade["score"]["earned"] == 5
    assert grade["questions"][0]["passed"] is True
    assert grade["hurdles"][0]["passed"] is True


def test_missing_results_award_no_points(tmp_path: Path) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
    grade = calculate_grade(pack, {})
    assert grade["score"]["earned"] == 0
    assert grade["questions"][0]["passed"] is False


def test_group_points_are_awarded_per_test_point(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    manifest = root / "pack.toml"
    text = manifest.read_text(encoding="utf-8")
    extra_test = (
        "[[questions.test_groups.tests]]\n"
        'id = "visible-boundary"\n'
        'argv = ["./q1"]\n'
        'expected_stdout = "ok\\n"\n'
        "expected_exit = 0\n\n"
        "[[questions.test_groups.tests]]\n"
        'id = "visible-edge"\n'
        'argv = ["./q1"]\n'
        'expected_stdout = "ok\\n"\n'
        "expected_exit = 0\n\n"
    )
    text = text.replace(
        '[[questions.test_groups]]\nid = "marking"',
        extra_test + '[[questions.test_groups]]\nid = "marking"',
    )
    manifest.write_text(text, encoding="utf-8")
    pack = load_pack(root)

    grade = calculate_grade(
        pack,
        {
            "q1": {
                "public": [
                    ResultClass.PASS,
                    ResultClass.WRONG_OUTPUT,
                    ResultClass.WRONG_OUTPUT,
                ],
                "marking": [ResultClass.WRONG_OUTPUT],
            }
        },
    )

    public = grade["questions"][0]["groups"][0]
    assert public["points_earned"] == pytest.approx(5 / 3)
    assert public["tests_passed"] == 1
    assert public["tests_available"] == 3
    assert public["passed"] is False
    assert public["tests"][0]["points_earned"] == pytest.approx(5 / 3)
    assert public["tests"][1]["points_earned"] == 0

    full_grade = calculate_grade(
        pack,
        {
            "q1": {
                "public": [ResultClass.PASS, ResultClass.PASS, ResultClass.PASS],
                "marking": [ResultClass.WRONG_OUTPUT],
            }
        },
    )
    assert full_grade["questions"][0]["groups"][0]["points_earned"] == 5
