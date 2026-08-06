from __future__ import annotations

from pathlib import Path

from test_pack import make_pack

from csetty.pack import load_pack
from csetty.supervisor import render_autotest_output


def _question(tmp_path: Path):
    return load_pack(make_pack(tmp_path / "pack")).question("q1")


def test_passing_autotest_summary_is_plain_without_tty_colour(tmp_path: Path) -> None:
    output = render_autotest_output(
        profile="comp1511",
        question=_question(tmp_path),
        result={
            "status": "PASS",
            "groups": [
                {
                    "id": "public",
                    "tests": [
                        {
                            "id": "positive",
                            "argv": ["./q1"],
                            "result": "PASS",
                            "stdout": "",
                            "stderr": "",
                            "detail": "",
                        }
                    ],
                }
            ],
        },
        colour=False,
    )
    assert "1511 c_check q1.c" in output
    assert "Test positive (./q1) - passed" in output
    assert output.endswith("1 tests passed 0 tests failed\n")
    assert "\x1b[" not in output


def test_wrong_output_includes_diff_input_and_reproduction(tmp_path: Path) -> None:
    output = render_autotest_output(
        profile="comp1511",
        question=_question(tmp_path),
        result={
            "status": "FAIL",
            "groups": [
                {
                    "id": "public",
                    "tests": [
                        {
                            "id": "negative",
                            "argv": ["./q1"],
                            "stdin": "-3\n",
                            "expected_stdout": "expected!\n",
                            "expected_stderr": "",
                            "result": "WRONG_OUTPUT",
                            "stdout": "actual\n",
                            "stderr": "",
                            "detail": "stdout did not match (exact)",
                        }
                    ],
                }
            ],
        },
        colour=True,
    )
    assert "failed (incorrect output)" in output
    assert "Your program wrote this to stdout:" in output
    assert "-actual" in output
    assert "+expected!" in output
    assert "Input used by this test:" in output
    assert "printf %s" in output
    assert "0 tests passed 1 tests failed" in output
    assert "\x1b[31m" in output
