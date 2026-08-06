from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from math import ceil
from time import monotonic
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime: ...

    def monotonic(self) -> float: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)

    def monotonic(self) -> float:
        return monotonic()


class DeadlineCountdown:
    """Monotonic live display, re-anchored from the persisted UTC deadline on startup."""

    def __init__(self, deadline: datetime | None, clock: Clock) -> None:
        self.deadline = None if deadline is None else deadline.astimezone(UTC)
        self.clock = clock
        self._monotonic_anchor = clock.monotonic()
        self._remaining_at_anchor = (
            None
            if self.deadline is None
            else max(0.0, (self.deadline - clock.now()).total_seconds())
        )

    def remaining_seconds(self) -> int | None:
        if self._remaining_at_anchor is None:
            return None
        elapsed = max(0.0, self.clock.monotonic() - self._monotonic_anchor)
        return max(0, ceil(self._remaining_at_anchor - elapsed))


@dataclass
class FrozenClock:
    current: datetime
    monotonic_value: float = 0.0

    def __post_init__(self) -> None:
        if self.current.tzinfo is None:
            self.current = self.current.replace(tzinfo=UTC)
        self.current = self.current.astimezone(UTC)

    def now(self) -> datetime:
        return self.current

    def monotonic(self) -> float:
        return self.monotonic_value

    def advance(self, *, seconds: float) -> None:
        self.current += timedelta(seconds=seconds)
        self.monotonic_value += seconds


def to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def from_iso(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
