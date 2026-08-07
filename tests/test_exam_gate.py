from __future__ import annotations

from io import StringIO

import pytest

import csetty.exam_gate as exam_gate_module
from csetty.errors import StateError
from csetty.exam_gate import clear_exam_terminal, run_exam_entry_gate, valid_zid


class TTYBuffer(StringIO):
    def isatty(self) -> bool:
        return True


def test_zid_format() -> None:
    assert valid_zid("z1234567")
    assert not valid_zid("z123456")
    assert not valid_zid("Z1234567")
    assert not valid_zid("z12345678")


def test_exam_terminal_clear_erases_screen_scrollback_and_homes_cursor() -> None:
    stream = TTYBuffer()
    clear_exam_terminal(stream)
    assert stream.getvalue() == "\x1b[2J\x1b[3J\x1b[H"


def test_exam_terminal_enables_windows_vt_before_writing_clear_sequence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []

    class OrderedTTYBuffer(TTYBuffer):
        def write(self, value: str) -> int:
            events.append("write")
            return super().write(value)

    stream = OrderedTTYBuffer()
    monkeypatch.setattr(
        exam_gate_module,
        "_enable_windows_virtual_terminal",
        lambda _output: events.append("enable-vt"),
    )

    clear_exam_terminal(stream)
    assert events == ["enable-vt", "write"]


def test_exam_terminal_clear_leaves_redirected_output_unchanged() -> None:
    stream = StringIO()
    clear_exam_terminal(stream)
    assert stream.getvalue() == ""


def test_exam_gate_reprompts_and_accepts(capsys: pytest.CaptureFixture[str]) -> None:
    answers = iter(("not-a-zid", "z1234567", "yes"))
    passwords = iter(("", "any characters are accepted"))
    cleared: list[bool] = []

    def clear() -> None:
        cleared.append(True)
        print("clear-marker")

    candidate_id = run_exam_entry_gate(
        "COMP1511",
        input_fn=lambda _prompt: next(answers),
        password_fn=lambda _prompt: next(passwords),
        clear_fn=clear,
    )
    assert candidate_id == "z1234567"
    assert cleared == [True]
    output = capsys.readouterr().out
    assert output.index("clear-marker") < output.index(
        "Welcome to the COMP1511 Exam Simulation"
    )
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
