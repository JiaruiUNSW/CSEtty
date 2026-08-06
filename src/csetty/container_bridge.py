from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

_ROOT = Path(os.environ.get("CSETTY_BRIDGE_DIR", "/run/csetty-bridge"))


def _color_enabled() -> bool:
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def request(operation: str, arguments: dict[str, Any], *, timeout: float = 600) -> int:
    try:
        session = json.loads((_ROOT / "session.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"csetty: exam supervisor is unavailable: {exc}", file=sys.stderr)
        return 4
    request_id = str(uuid.uuid4())
    request_arguments = dict(arguments)
    if operation == "autotest" and _color_enabled():
        request_arguments["color"] = True
    payload = {
        "protocol": 1,
        "request_id": request_id,
        "attempt_id": session["attempt_id"],
        "session_token": session["session_token"],
        "operation": operation,
        "arguments": request_arguments,
    }
    requests = _ROOT / "requests"
    responses = _ROOT / "responses"
    temporary = requests / f".{request_id}.tmp"
    target = requests / f"{request_id}.json"
    temporary.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    os.replace(temporary, target)
    response_path = responses / f"{request_id}.json"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if response_path.is_file() and not response_path.is_symlink():
            try:
                response = json.loads(response_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                time.sleep(0.05)
                continue
            response_path.unlink(missing_ok=True)
            if response.get("stdout"):
                print(response["stdout"], end="")
            if response.get("stderr"):
                print(response["stderr"], end="", file=sys.stderr)
            return int(response.get("exit_code", 5))
        time.sleep(0.05)
    print("csetty: timed out waiting for the exam supervisor", file=sys.stderr)
    return 4


def _exam(arguments: list[str]) -> int:
    command = arguments[0] if arguments else "help"
    rest = arguments[1:]
    if command == "help":
        print("exam help|status|questions|submissions [ACTIVITY]|finish")
        return 0
    if command == "status" and not rest:
        return request("status", {})
    if command == "questions" and not rest:
        return request("questions", {})
    if command == "submissions" and len(rest) <= 1:
        return request("submissions", {"activity": rest[0] if rest else None})
    if command == "finish":
        assume_yes = rest == ["--yes"]
        if rest and not assume_yes:
            print("usage: exam finish [--yes]", file=sys.stderr)
            return 2
        if not assume_yes:
            if not sys.stdin.isatty():
                print("exam finish: use --yes when stdin is not a TTY", file=sys.stderr)
                return 2
            try:
                answer = input("Finish this attempt permanently? [y/N] ")
            except EOFError:
                print("Attempt not finished.")
                return 1
            if answer.strip().lower() not in {"y", "yes"}:
                print("Attempt not finished.")
                return 1
        return request("finish", {})
    print(f"exam: unknown or invalid command: {command}", file=sys.stderr)
    return 2


def _comp1511(arguments: list[str]) -> int:
    if not arguments:
        print("usage: 1511 fetch|autotest|check ...", file=sys.stderr)
        return 2
    command, *rest = arguments
    if command == "fetch":
        force = False
        activities = []
        for argument in rest:
            if argument == "--force":
                if force:
                    print("1511: --force was specified more than once", file=sys.stderr)
                    return 2
                force = True
            elif argument.startswith("-"):
                print(f"1511: invalid fetch option: {argument}", file=sys.stderr)
                return 2
            else:
                activities.append(argument)
        if len(activities) <= 1:
            return request(
                "fetch", {"activity": activities[0] if activities else None, "force": force}
            )
    if command == "autotest" and 1 <= len(rest) <= 2:
        return request(
            "autotest",
            {"activity": rest[0], "selector": rest[1] if len(rest) == 2 else None},
        )
    if command == "check" and not rest:
        return request("check", {})
    print(f"1511: invalid command: {command}", file=sys.stderr)
    return 2


def _comp1521(arguments: list[str]) -> int:
    if not arguments:
        print("usage: 1521 fetch|autotest|mipsy|check|classrun ...", file=sys.stderr)
        return 2
    command, *rest = arguments
    if command == "fetch" and len(rest) == 1:
        return request("fetch", {"activity": None, "force": False, "pack_name": rest[0]})
    if command == "autotest" and 1 <= len(rest) <= 2:
        return request(
            "autotest", {"activity": rest[0], "selector": rest[1] if len(rest) == 2 else None}
        )
    if command == "mipsy" and rest:
        runner_arguments = ["mipsy", rest[0]]
        if len(rest) > 1:
            # The course-facing form is `1521 mipsy FILE [ARG ...]`, while the
            # underlying runner uses `--` to distinguish program arguments
            # from additional assembler inputs.
            if rest[1] == "--":
                runner_arguments.extend(rest[1:])
            else:
                runner_arguments.extend(("--", *rest[1:]))
        try:
            return subprocess.run(runner_arguments, check=False).returncode
        except FileNotFoundError:
            print("1521: mipsy is not installed in this image", file=sys.stderr)
            return 4
    if command == "check" and not rest:
        return request("check", {})
    if command == "classrun" and rest:
        if rest[0] in {"-check", "check"} and len(rest) == 1:
            return request("check", {})
        if len(rest) == 1:
            return request("submission", {"activity": rest[0]})
    print(f"1521: invalid command: {command}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("csetty container command shim: missing command", file=sys.stderr)
        return 2
    command, *rest = args
    if command == "exam":
        return _exam(rest)
    if command == "1511":
        return _comp1511(rest)
    if command == "1521":
        return _comp1521(rest)
    if command == "autotest" and 1 <= len(rest) <= 2:
        return request(
            "autotest", {"activity": rest[0], "selector": rest[1] if len(rest) == 2 else None}
        )
    if command == "submit" and rest:
        return request("submit", {"activity": rest[0], "files": rest[1:]})
    if command == "check" and not rest:
        return request("check", {})
    print(f"unknown exam command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
