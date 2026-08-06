from __future__ import annotations

from datetime import UTC, datetime, timedelta

from csetty.clock import DeadlineCountdown, FrozenClock, from_iso, to_iso


def test_frozen_clock_and_iso_round_trip() -> None:
    start = datetime(2026, 8, 5, 10, 0, tzinfo=UTC)
    clock = FrozenClock(start)
    clock.advance(seconds=12.5)
    assert clock.monotonic() == 12.5
    assert from_iso(to_iso(clock.now())) == clock.now()


def test_deadline_countdown_uses_monotonic_time_until_restart() -> None:
    start = datetime(2026, 8, 5, 10, 0, tzinfo=UTC)
    source = FrozenClock(start, monotonic_value=100)
    countdown = DeadlineCountdown(start + timedelta(seconds=60), source)
    assert countdown.remaining_seconds() == 60

    source.current += timedelta(hours=1)
    assert countdown.remaining_seconds() == 60
    source.monotonic_value += 10.25
    assert countdown.remaining_seconds() == 50

    restarted = DeadlineCountdown(start + timedelta(seconds=60), source)
    assert restarted.remaining_seconds() == 0


def test_untimed_countdown_has_no_remaining_value() -> None:
    source = FrozenClock(datetime(2026, 8, 5, 10, 0, tzinfo=UTC))
    assert DeadlineCountdown(None, source).remaining_seconds() is None
