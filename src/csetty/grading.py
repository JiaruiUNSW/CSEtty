from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from .models import ResultClass
from .pack import Pack


def _number(value: Decimal) -> int | float:
    integral = value.to_integral_value()
    return int(integral) if value == integral else float(value)


def calculate_grade(
    pack: Pack,
    group_results: Mapping[str, Mapping[str, Sequence[ResultClass | str]]],
) -> dict[str, Any]:
    questions: list[dict[str, Any]] = []
    question_passes: dict[str, bool] = {}
    total_earned = Decimal(0)
    total_available = Decimal(0)

    for question in pack.questions:
        question_earned = Decimal(0)
        group_reports: list[dict[str, Any]] = []
        supplied_groups = group_results.get(question.id, {})
        for group in question.test_groups:
            supplied = tuple(ResultClass(item) for item in supplied_groups.get(group.id, ()))
            passed = len(supplied) == len(group.tests) and all(
                result is ResultClass.PASS for result in supplied
            )
            earned = group.points if passed else Decimal(0)
            question_earned += earned
            total_available += group.points
            group_reports.append(
                {
                    "id": group.id,
                    "visibility": group.visibility.value,
                    "points_earned": _number(earned),
                    "points_available": _number(group.points),
                    "passed": passed,
                    "results": [result.value for result in supplied],
                }
            )
        passed_question = question_earned >= question.pass_points
        question_passes[question.id] = passed_question
        total_earned += question_earned
        questions.append(
            {
                "id": question.id,
                "title": question.title,
                "points_earned": _number(question_earned),
                "automatic_points": _number(question.automatic_points),
                "total_points": _number(question.points),
                "not_automatically_assessed": _number(question.points - question.automatic_points),
                "pass_points": _number(question.pass_points),
                "passed": passed_question,
                "groups": group_reports,
            }
        )

    hurdles: list[dict[str, Any]] = []
    for hurdle in pack.hurdles:
        passed_questions = [item for item in hurdle.question_ids if question_passes[item]]
        hurdles.append(
            {
                "id": hurdle.id,
                "label": hurdle.label,
                "passed": len(passed_questions) >= hurdle.min_passed_questions,
                "passed_questions": passed_questions,
                "required": hurdle.min_passed_questions,
                "eligible_questions": list(hurdle.question_ids),
            }
        )

    return {
        "schema_version": 1,
        "notice": "Local simulator estimate; this is not an official UNSW mark.",
        "pack": {"id": pack.id, "version": pack.version, "digest": pack.digest},
        "score": {
            "earned": _number(total_earned),
            "automatically_available": _number(total_available),
            "total": _number(pack.total_points),
            "not_automatically_assessed": _number(pack.total_points - total_available),
        },
        "questions": questions,
        "hurdles": hurdles,
    }


def render_grade_text(report: Mapping[str, Any]) -> str:
    score = report["score"]
    lines = [
        str(report["notice"]),
        (
            f"Automatic score: {score['earned']}/{score['automatically_available']} "
            f"(paper total: {score['total']})"
        ),
    ]
    if score["not_automatically_assessed"]:
        lines.append(f"Not automatically assessed: {score['not_automatically_assessed']} points")
    lines.append("")
    for question in report["questions"]:
        state = "PASS" if question["passed"] else "NOT PASSED"
        lines.append(
            f"{question['id']}: {question['points_earned']}/{question['automatic_points']} "
            f"automatic points — {state}"
        )
        for group in question["groups"]:
            group_state = "PASS" if group["passed"] else "FAIL"
            lines.append(
                f"  {group['id']} [{group['visibility']}]: {group_state} "
                f"({group['points_earned']}/{group['points_available']})"
            )
    if report["hurdles"]:
        lines.extend(("", "Hurdles:"))
        for hurdle in report["hurdles"]:
            state = "PASS" if hurdle["passed"] else "FAIL"
            lines.append(f"  {hurdle['label']}: {state}")
    return "\n".join(lines)
