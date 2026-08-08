from __future__ import annotations

import pytest

import csetty.container_bridge as container_bridge
from csetty.cli import _check_start_options, _parser
from csetty.errors import UsageError
from csetty.models import AttemptMode


def test_exam_mode_rejects_network_and_skip_reading() -> None:
    parser = _parser()
    with pytest.raises(UsageError, match="network none"):
        _check_start_options(
            parser.parse_args(["start", "pack", "--mode", "exam", "--network", "on"])
        )
    with pytest.raises(UsageError, match="skip-reading"):
        _check_start_options(
            parser.parse_args(["start", "pack", "--mode", "exam", "--skip-reading"])
        )


def test_start_uses_pack_default_mode_unless_explicitly_overridden() -> None:
    parser = _parser()
    generated = parser.parse_args(["start", "generated-pack"])
    mode, timed, network = _check_start_options(generated, default_mode="exam")
    assert (mode, timed, network) == (AttemptMode.EXAM, True, "none")

    practice = parser.parse_args(
        ["start", "generated-pack", "--mode", "practice"]
    )
    mode, timed, network = _check_start_options(practice, default_mode="exam")
    assert (mode, timed, network) == (AttemptMode.PRACTICE, False, "none")


def test_1511_fetch_force_and_autotest_selector(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = []

    def fake_request(operation, arguments, **_kwargs):
        captured.append((operation, arguments))
        return 0

    monkeypatch.setattr(container_bridge, "request", fake_request)
    assert container_bridge._comp1511(["fetch", "q1", "--force"]) == 0
    assert captured[-1] == ("fetch", {"activity": "q1", "force": True})
    assert container_bridge._comp1511(["autotest", "q1", "public"]) == 0
    assert captured[-1] == (
        "autotest",
        {"activity": "q1", "selector": "public"},
    )


def test_bank_verify_command_is_exposed() -> None:
    args = _parser().parse_args(["bank", "verify", "comp1521"])
    assert args.command == "bank"
    assert args.bank_command == "verify"
    assert str(args.path) == "comp1521"
