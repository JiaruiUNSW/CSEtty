from __future__ import annotations

import getpass
import os
import re
import sys
from collections.abc import Callable
from typing import TextIO

from .errors import StateError, UsageError

_ZID_PATTERN = re.compile(r"^z[0-9]{7}$")
_CLEAR_TERMINAL = "\x1b[2J\x1b[3J\x1b[H"
_ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004


def valid_zid(value: str) -> bool:
    return _ZID_PATTERN.fullmatch(value) is not None


def _enable_windows_virtual_terminal(output: TextIO) -> None:
    """Best-effort enable ANSI processing for an attached Windows console."""
    if os.name != "nt":
        return
    try:
        import ctypes
        import importlib

        msvcrt = importlib.import_module("msvcrt")
        handle = msvcrt.get_osfhandle(output.fileno())
        kernel32 = getattr(ctypes, "windll").kernel32  # noqa: B009
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(
                handle,
                mode.value | _ENABLE_VIRTUAL_TERMINAL_PROCESSING,
            )
    except (AttributeError, ImportError, OSError, ValueError):
        # Windows Terminal, ConPTY, and POSIX-like terminals may already handle
        # ANSI even when no Win32 console mode is available for this stream.
        return


def clear_exam_terminal(stream: TextIO | None = None) -> None:
    """Clear the visible screen and scrollback before an interactive exam gate."""
    output = sys.stdout if stream is None else stream
    if not output.isatty():
        return
    _enable_windows_virtual_terminal(output)
    output.write(_CLEAR_TERMINAL)
    output.flush()


def run_exam_entry_gate(
    course: str,
    *,
    input_fn: Callable[[str], str] = input,
    password_fn: Callable[[str], str] = getpass.getpass,
    clear_fn: Callable[[], None] = clear_exam_terminal,
) -> str:
    clear_fn()
    print("=" * 60)
    print(f"Welcome to the {course} Exam Simulation")
    print("=" * 60)
    print("This is a local CSEExamTTY simulation, not UNSW authentication.")

    while True:
        try:
            candidate_id = input_fn("zID (z followed by 7 digits): ").strip()
        except EOFError as exc:
            raise UsageError("exam sign-in requires an interactive terminal") from exc
        if valid_zid(candidate_id):
            break
        print("Invalid zID. Enter a lowercase z followed by exactly 7 digits.")

    while True:
        try:
            password = password_fn(
                "zPassword (simulation only; do not enter your real UNSW zPass): "
            )
        except EOFError as exc:
            raise UsageError("exam sign-in requires an interactive terminal") from exc
        if password:
            break
        print("zPassword must contain at least one character.")
    # The local simulator deliberately does not authenticate, retain, hash, or log this value.
    del password

    print("\nIMPORTANT ACKNOWLEDGEMENT")
    print(
        "I understand that this mock exam system is neither made nor managed by the "
        "UNSW School of Computer Science and Engineering."
    )
    print("\nACADEMIC INTEGRITY AND EXAMINATION CONDITIONS")
    print("By continuing, I declare that:")
    print("1. Every answer I submit will be entirely my own work.")
    print("2. I will not communicate with, seek help from, or give help to another person.")
    print("3. I will not use generative AI, code-synthesis tools, messaging, or active help.")
    print("4. I will access only the files, documentation, and resources permitted by the paper.")
    print("5. I will keep the paper, my answers, and my credentials private.")
    print("6. I will not write during reading time or continue working after time expires.")
    print("7. I understand deliberate breaches would violate official exam conditions and may")
    print("   amount to academic misconduct in a real exam.")
    print("\nLOCAL SIMULATION NOTICE")
    print("CSEExamTTY does not authenticate, invigilate, report misconduct, or submit to UNSW.")
    print("Only locally persisted submissions made before the deadline can be marked.")
    try:
        accepted = input_fn(
            'Type "yes" to acknowledge the disclaimer, accept these conditions, and enter: '
        )
    except EOFError as exc:
        raise UsageError("exam conditions require an interactive terminal") from exc
    if accepted.strip().lower() != "yes":
        raise StateError("exam conditions were not accepted; no attempt was created")
    print(f"\nSigned in as {candidate_id}. Preparing the read-only exam paper...\n")
    return candidate_id
