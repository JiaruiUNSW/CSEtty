from __future__ import annotations

import pytest

from csetty.errors import StateError
from csetty.exam_gate import run_exam_entry_gate, valid_zid


def test_zid_format() -> None:
    assert valid_zid("z1234567")
    assert not valid_zid("z123456")
    assert not valid_zid("Z1234567")
    assert not valid_zid("z12345678")


def test_exam_gate_reprompts_and_accepts(capsys: pytest.CaptureFixture[str]) -> None:
    answers = iter(("not-a-zid", "z1234567", "yes"))
    passwords = iter(("", "any characters are accepted"))
    candidate_id = run_exam_entry_gate(
        "COMP1511",
        input_fn=lambda _prompt: next(answers),
        password_fn=lambda _prompt: next(passwords),
    )
    assert candidate_id == "z1234567"
    output = capsys.readouterr().out
    assert "Welcome to the COMP1511 Exam Simulation" in output
    assert "Invalid zID" in output
    assert (
        "neither made nor managed by the UNSW School of Computer Science and Engineering" in output
    )
    assert "ACADEMIC INTEGRITY AND EXAMINATION CONDITIONS" in output
    assert "generative AI" in output
    assert "academic misconduct" in output
    assert "modelled on publicly available UNSW exam rules" not in output


def test_exam_gate_requires_exact_yes() -> None:
    answers = iter(("z7654321", "y"))
    with pytest.raises(StateError, match="no attempt was created"):
        run_exam_entry_gate(
            "COMP1521",
            input_fn=lambda _prompt: next(answers),
            password_fn=lambda _prompt: "anything",
        )
