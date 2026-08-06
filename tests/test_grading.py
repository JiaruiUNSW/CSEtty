from __future__ import annotations

from pathlib import Path

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
