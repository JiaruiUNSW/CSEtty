from __future__ import annotations

import json
import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from contextlib import suppress
from pathlib import Path, PurePosixPath
from typing import Any


def _copy_tree_without_links(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    source_root = source.resolve()
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ValueError(
                f"symlinks are not accepted in judge input: {path.relative_to(source)}"
            )
        relative = path.relative_to(source)
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            if not path.resolve().is_relative_to(source_root):
                raise ValueError(f"input escapes source root: {relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def _limit_child() -> None:
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    os.setsid()


def _execute(
    argv: list[str],
    *,
    cwd: Path,
    stdin: str,
    timeout_ms: int,
    output_limit: int,
) -> dict[str, Any]:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="csetty-capture-") as capture_name:
        capture = Path(capture_name)
        stdin_path = capture / "stdin"
        stdout_path = capture / "stdout"
        stderr_path = capture / "stderr"
        stdin_path.write_bytes(stdin.encode())
        try:
            with (
                stdin_path.open("rb") as stdin_stream,
                stdout_path.open("wb") as stdout_stream,
                stderr_path.open("wb") as stderr_stream,
            ):
                process = subprocess.Popen(
                    argv,
                    cwd=cwd,
                    stdin=stdin_stream,
                    stdout=stdout_stream,
                    stderr=stderr_stream,
                    start_new_session=False,
                    preexec_fn=_limit_child,
                )
                deadline = started + timeout_ms / 1000
                timed_out = False
                output_limited = False
                while process.poll() is None:
                    if (
                        stdout_path.stat().st_size > output_limit
                        or stderr_path.stat().st_size > output_limit
                    ):
                        output_limited = True
                    elif time.monotonic() >= deadline:
                        timed_out = True
                    else:
                        time.sleep(0.01)
                        continue
                    with suppress(ProcessLookupError):
                        os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=2)
        except FileNotFoundError as exc:
            return {
                "exit_code": None,
                "timed_out": False,
                "output_limited": False,
                "duration_ms": int((time.monotonic() - started) * 1000),
                "stdout": "",
                "stderr": str(exc),
                "spawn_error": True,
            }

        stdout_size = stdout_path.stat().st_size
        stderr_size = stderr_path.stat().st_size
        stdout = stdout_path.read_bytes()[:output_limit]
        stderr = stderr_path.read_bytes()[:output_limit]
        output_limited = output_limited or stdout_size > output_limit or stderr_size > output_limit

    return {
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "output_limited": output_limited,
        "duration_ms": int((time.monotonic() - started) * 1000),
        "stdout": stdout.decode("utf-8", errors="replace"),
        "stderr": stderr.decode("utf-8", errors="replace"),
        "spawn_error": False,
    }


def _normalize(value: str, comparison: str, selected: str | None) -> str:
    if comparison == "exact":
        return value
    if comparison == "ignore_trailing_whitespace":
        return "\n".join(line.rstrip() for line in value.splitlines())
    if comparison == "ignore_whitespace":
        return "".join(value.split())
    if comparison == "ignore_case":
        return value.casefold()
    if comparison == "selected_characters":
        accepted = set(selected or "")
        return "".join(character for character in value if character in accepted)
    raise ValueError(f"unsupported comparison: {comparison}")


def _regular_file_under(root: Path, relative: str) -> Path | None:
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    candidate = root
    for part in path.parts:
        candidate /= part
        if candidate.is_symlink():
            return None
    if not candidate.is_file():
        return None
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        return None
    return resolved if resolved.is_relative_to(root.resolve()) else None


def _classify(test: dict[str, Any], execution: dict[str, Any], work: Path) -> tuple[str, str]:
    if execution["spawn_error"]:
        return "INTERNAL_ERROR", execution["stderr"]
    if execution["timed_out"]:
        return "TIMEOUT", "wall-clock timeout exceeded"
    if execution["output_limited"]:
        return "OUTPUT_LIMIT", "captured output exceeded the configured limit"
    expected_exit = test.get("expected_exit")
    actual_exit = execution["exit_code"]
    if expected_exit is not None and actual_exit != expected_exit:
        if expected_exit == 0 and actual_exit not in {0, None}:
            return "RUNTIME_ERROR", f"program exited with status {actual_exit}"
        return "WRONG_EXIT_STATUS", f"expected exit {expected_exit}, got {actual_exit}"
    comparison = test.get("comparison", "exact")
    selected = test.get("selected_characters")
    for stream_name in ("stdout", "stderr"):
        expected = test.get(f"expected_{stream_name}")
        if expected is not None and _normalize(
            execution[stream_name], comparison, selected
        ) != _normalize(expected, comparison, selected):
            return "WRONG_OUTPUT", f"{stream_name} did not match ({comparison})"
    for expected_file in test.get("expected_files", []):
        path = _regular_file_under(work, expected_file["path"])
        if path is None:
            return "WRONG_OUTPUT", f"expected output file was not created: {expected_file['path']}"
        actual = path.read_text(encoding="utf-8", errors="replace")
        if _normalize(actual, comparison, selected) != _normalize(
            expected_file["content"], comparison, selected
        ):
            return "WRONG_OUTPUT", f"output file did not match: {expected_file['path']}"
    return "PASS", ""


def run(config: dict[str, Any]) -> dict[str, Any]:
    source = Path(config.get("source_dir", "/submission"))
    pack = Path(config.get("pack_dir", "/pack"))
    output_limit = int(config.get("output_limit_kb", 256)) * 1024
    with tempfile.TemporaryDirectory(prefix="csetty-judge-") as temporary:
        root = Path(temporary)
        base = root / "base"
        _copy_tree_without_links(source, base)
        build = None
        build_argv = list(config.get("build_argv", []))
        if build_argv:
            build = _execute(
                build_argv,
                cwd=base,
                stdin="",
                timeout_ms=int(config.get("build_timeout_ms", 30_000)),
                output_limit=output_limit,
            )
            if (
                build["spawn_error"]
                or build["timed_out"]
                or build["output_limited"]
                or build["exit_code"] != 0
            ):
                if build["spawn_error"]:
                    result_class = "INTERNAL_ERROR"
                elif build["timed_out"]:
                    result_class = "TIMEOUT"
                elif build["output_limited"]:
                    result_class = "OUTPUT_LIMIT"
                else:
                    result_class = "COMPILE_ERROR"
                groups = []
                for group in config["groups"]:
                    groups.append(
                        {
                            "id": group["id"],
                            "visibility": group["visibility"],
                            "tests": [
                                {
                                    "id": test["id"],
                                    "argv": test["argv"],
                                    "stdin": test.get("stdin", ""),
                                    "expected_stdout": test.get("expected_stdout"),
                                    "expected_stderr": test.get("expected_stderr"),
                                    "expected_exit": test.get("expected_exit"),
                                    "result": result_class,
                                    "duration_ms": 0,
                                    "exit_code": None,
                                    "stdout": "",
                                    "stderr": build["stderr"],
                                    "detail": "build failed",
                                }
                                for test in group["tests"]
                            ],
                        }
                    )
                return {
                    "status": result_class,
                    "build": build,
                    "build_argv": build_argv,
                    "groups": groups,
                }

        groups_result: list[dict[str, Any]] = []
        overall = "PASS"
        for group in config["groups"]:
            outcomes: list[dict[str, Any]] = []
            for test in group["tests"]:
                work = root / f"work-{group['id']}-{test['id']}"
                _copy_tree_without_links(base, work)
                for fixture in test.get("fixtures", []):
                    source_fixture = pack / fixture["source"]
                    target = work / fixture["path"]
                    if source_fixture.is_symlink() or not source_fixture.is_file():
                        raise ValueError(f"invalid fixture: {fixture['source']}")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source_fixture, target)
                execution = _execute(
                    list(test["argv"]),
                    cwd=work,
                    stdin=test.get("stdin", ""),
                    timeout_ms=int(test.get("timeout_ms", 2000)),
                    output_limit=output_limit,
                )
                classification, detail = _classify(test, execution, work)
                if classification != "PASS":
                    overall = "FAIL" if classification != "INTERNAL_ERROR" else "INTERNAL_ERROR"
                outcomes.append(
                    {
                        "id": test["id"],
                        "argv": test["argv"],
                        "stdin": test.get("stdin", ""),
                        "expected_stdout": test.get("expected_stdout"),
                        "expected_stderr": test.get("expected_stderr"),
                        "expected_exit": test.get("expected_exit"),
                        "result": classification,
                        "duration_ms": execution["duration_ms"],
                        "exit_code": execution["exit_code"],
                        "stdout": execution["stdout"],
                        "stderr": execution["stderr"],
                        "detail": detail,
                    }
                )
            groups_result.append(
                {"id": group["id"], "visibility": group["visibility"], "tests": outcomes}
            )
        return {
            "status": overall,
            "build": build,
            "build_argv": build_argv,
            "groups": groups_result,
        }


def main() -> int:
    try:
        config = json.load(sys.stdin)
        result = run(config)
    except Exception as exc:  # judge failures must remain distinct from student failures
        result = {"status": "INTERNAL_ERROR", "build": None, "groups": [], "error": str(exc)}
    json.dump(result, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if result["status"] != "INTERNAL_ERROR" else 5


if __name__ == "__main__":
    raise SystemExit(main())
