from __future__ import annotations

from types import SimpleNamespace

import pytest

import csetty.container_bridge as commands


def test_exam_command_request_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[tuple[str, dict[str, object]]] = []

    def fake_request(operation: str, arguments: dict[str, object], **_kwargs: object) -> int:
        captured.append((operation, arguments))
        return 0

    monkeypatch.setattr(commands, "request", fake_request)
    assert commands._exam(["status"]) == 0
    assert commands._exam(["questions"]) == 0
    assert commands._exam(["submissions"]) == 0
    assert commands._exam(["submissions", "prac_q1"]) == 0
    assert commands._exam(["finish", "--yes"]) == 0
    assert captured == [
        ("status", {}),
        ("questions", {}),
        ("submissions", {"activity": None}),
        ("submissions", {"activity": "prac_q1"}),
        ("finish", {}),
    ]


def test_course_command_request_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[tuple[str, dict[str, object]]] = []

    def fake_request(operation: str, arguments: dict[str, object], **_kwargs: object) -> int:
        captured.append((operation, arguments))
        return 0

    monkeypatch.setattr(commands, "request", fake_request)
    assert commands._comp1511(["fetch"]) == 0
    assert commands._comp1511(["fetch", "q1", "--force"]) == 0
    assert commands._comp1511(["autotest", "q1", "edge"]) == 0
    assert commands._comp1511(["check"]) == 0
    assert commands._comp1521(["fetch", "comp1521-original-a"]) == 0
    assert commands._comp1521(["autotest", "q1", "public"]) == 0
    assert commands._comp1521(["check"]) == 0
    assert commands._comp1521(["classrun", "-check"]) == 0
    assert commands._comp1521(["classrun", "q1"]) == 0
    assert captured == [
        ("fetch", {"activity": None, "force": False}),
        ("fetch", {"activity": "q1", "force": True}),
        ("autotest", {"activity": "q1", "selector": "edge"}),
        ("check", {}),
        (
            "fetch",
            {
                "activity": None,
                "force": False,
                "pack_name": "comp1521-original-a",
            },
        ),
        ("autotest", {"activity": "q1", "selector": "public"}),
        ("check", {}),
        ("check", {}),
        ("submission", {"activity": "q1"}),
    ]


def test_common_autotest_submit_and_check_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[tuple[str, dict[str, object]]] = []

    def fake_request(operation: str, arguments: dict[str, object], **_kwargs: object) -> int:
        captured.append((operation, arguments))
        return 0

    monkeypatch.setattr(commands, "request", fake_request)
    assert commands.main(["autotest", "q1", "basic"]) == 0
    assert commands.main(["submit", "q1", "answer.c"]) == 0
    assert commands.main(["check"]) == 0
    assert captured == [
        ("autotest", {"activity": "q1", "selector": "basic"}),
        ("submit", {"activity": "q1", "files": ["answer.c"]}),
        ("check", {}),
    ]


def test_mipsy_is_executed_as_an_argument_array(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[list[str]] = []

    def fake_run(argv: list[str], *, check: bool) -> SimpleNamespace:
        assert check is False
        captured.append(argv)
        return SimpleNamespace(returncode=7)

    monkeypatch.setattr(commands.subprocess, "run", fake_run)
    assert commands._comp1521(["mipsy", "program.s", "a value", "; touch nope"]) == 7
    assert captured == [["mipsy", "program.s", "--", "a value", "; touch nope"]]


def test_mipsy_preserves_an_explicit_program_argument_separator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[list[str]] = []

    def fake_run(argv: list[str], *, check: bool) -> SimpleNamespace:
        assert check is False
        captured.append(argv)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(commands.subprocess, "run", fake_run)
    assert commands._comp1521(["mipsy", "program.s", "--", "arg"]) == 0
    assert captured == [["mipsy", "program.s", "--", "arg"]]


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (["give", "cs1521", "q1", "q1.c"], "unknown exam command: give"),
        (["1511", "fetch-prac", "q1", "q2"], "1511: invalid command"),
        (["1521", "classrun", "-check", "q1", "extra"], "1521: invalid command"),
        (["exam", "finish", "unexpected"], "usage: exam finish"),
    ],
)
def test_invalid_command_forms_have_stable_exit_code_and_error(
    argv: list[str], message: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert commands.main(argv) == 2
    assert message in capsys.readouterr().err
