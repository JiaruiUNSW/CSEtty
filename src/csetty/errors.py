from __future__ import annotations


class CSETTYError(Exception):
    """A user-facing error with a stable CLI exit code."""

    def __init__(self, message: str, *, exit_code: int = 5) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class UsageError(CSETTYError):
    def __init__(self, message: str) -> None:
        super().__init__(message, exit_code=2)


class StateError(CSETTYError):
    def __init__(self, message: str) -> None:
        super().__init__(message, exit_code=3)


class ToolUnavailableError(CSETTYError):
    def __init__(self, message: str) -> None:
        super().__init__(message, exit_code=4)


class ValidationError(CSETTYError):
    def __init__(self, message: str) -> None:
        super().__init__(message, exit_code=5)
