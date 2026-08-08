#!/usr/bin/env python3
"""One-shot, reproducible authoring upgrade for the bundled question banks.

The script is intentionally separate from the student-facing runtime.  It adds
one genuinely different, reference-derived edge case to legacy four-point
questions and expands terse solution notes with a worked execution trace.  It
is idempotent so maintainers can safely rerun it while curating the bank.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from csetty_mips import SourceUnit, assemble
from csetty_mips.machine import Machine

ROOT = Path(__file__).resolve().parents[1]
QUESTION_ROOT = ROOT / "question_bank"
EXTRA_TEST_ID = "extended-edge"
MINIMUM_TEST_POINTS = 5
INTEGER = re.compile(r"(?<![A-Za-z0-9_])-?\d+(?![A-Za-z0-9_])")
HEX_BYTES = re.compile(r"(?:[0-9A-Fa-f]{2})+")


@dataclass(frozen=True)
class Execution:
    exit_code: int
    stdout: str
    stderr: str
    expected_files: tuple[str, ...]


@dataclass(frozen=True)
class Candidate:
    test: dict[str, Any]
    fixture_writes: tuple[tuple[Path, bytes], ...] = ()


def _question_manifests() -> Iterator[Path]:
    yield from sorted(QUESTION_ROOT.glob("*/questions/*/question.json"))


def _replace_span(text: str, start: int, end: int, replacement: str) -> str:
    return f"{text[:start]}{replacement}{text[end:]}"


def _mutated_numbers(text: str) -> Iterator[str]:
    matches = list(INTEGER.finditer(text))
    for match in reversed(matches):
        value = int(match.group())
        replacements = (1, -1, 2) if value == 0 else (value + 1, value - 1, value * 2)
        for replacement in replacements:
            if replacement != value:
                yield _replace_span(text, match.start(), match.end(), str(replacement))


def _mutated_characters(text: str) -> Iterator[str]:
    for index in range(len(text) - 1, -1, -1):
        character = text[index]
        if "a" <= character <= "y":
            yield _replace_span(text, index, index + 1, chr(ord(character) + 1))
        elif character == "z":
            yield _replace_span(text, index, index + 1, "a")
        elif "A" <= character <= "Y":
            yield _replace_span(text, index, index + 1, chr(ord(character) + 1))
        elif character == "Z":
            yield _replace_span(text, index, index + 1, "A")


def _mutated_hex(text: str) -> Iterator[str]:
    if not HEX_BYTES.fullmatch(text):
        return
    for index in range(len(text) - 2, -1, -2):
        value = int(text[index : index + 2], 16)
        replacement = f"{(value + 1) & 0xFF:02x}"
        yield _replace_span(text, index, index + 2, replacement)


def _mutated_bytes(content: bytes) -> Iterator[bytes]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = ""
    if text:
        for candidate in _mutated_numbers(text):
            yield candidate.encode()
        for candidate in _mutated_characters(text):
            yield candidate.encode()
    if content:
        index = (
            len(content) - 2 if content.endswith(b"\n") and len(content) > 1 else len(content) - 1
        )
        changed = bytearray(content)
        changed[index] = (changed[index] + 1) % 256
        yield bytes(changed)
    else:
        yield b"0\n"


def _candidate_tests(question_root: Path, raw: dict[str, Any]) -> Iterator[Candidate]:
    tests = [test for group in reversed(raw["test_groups"]) for test in reversed(group["tests"])]
    for source_test in tests:
        stdin = source_test.get("stdin", "")
        for mutated in (*_mutated_numbers(stdin), *_mutated_characters(stdin)):
            test = copy.deepcopy(source_test)
            test["id"] = EXTRA_TEST_ID
            test["stdin"] = mutated
            yield Candidate(test)

        argv = list(source_test["argv"])
        protected_prefix = 2 if raw["kind"] == "mips_program" else 1
        for index in range(len(argv) - 1, protected_prefix - 1, -1):
            value = argv[index]
            mutations = (
                *_mutated_numbers(value),
                *_mutated_hex(value),
                *_mutated_characters(value),
            )
            for mutated in mutations:
                test = copy.deepcopy(source_test)
                test["id"] = EXTRA_TEST_ID
                test["argv"][index] = mutated
                yield Candidate(test)

        for fixture_index, fixture in enumerate(source_test.get("fixtures", [])):
            source = question_root / fixture["source"]
            content = source.read_bytes()
            for mutation_index, mutated in enumerate(_mutated_bytes(content), start=1):
                suffix = source.suffix or ".dat"
                relative = Path("tests") / (
                    f"{EXTRA_TEST_ID}-{fixture_index + 1}-{mutation_index}{suffix}"
                )
                test = copy.deepcopy(source_test)
                test["id"] = EXTRA_TEST_ID
                test["fixtures"][fixture_index]["source"] = relative.as_posix()
                yield Candidate(test, ((relative, mutated),))


def _safe_output_path(work: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe expected-file path: {relative}")
    return work / path


@contextmanager
def _c_runner(
    question_root: Path, raw: dict[str, Any]
) -> Iterator[Callable[[dict[str, Any], tuple[tuple[Path, bytes], ...]], Execution]]:
    with tempfile.TemporaryDirectory(prefix="csetty-bank-author-") as temporary_name:
        temporary = Path(temporary_name)
        base = temporary / "base"
        base.mkdir()
        for submission in raw["submission_files"]:
            source = question_root / "reference" / submission
            target = base / submission
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        build = list(raw["build"]["argv"])
        if build[0] == "dcc":
            build[0] = os.environ.get("CC", "cc")
        completed = subprocess.run(
            build,
            cwd=base,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"cannot compile {raw['id']}:\n{completed.stdout}{completed.stderr}")

        def run(test: dict[str, Any], fixture_writes: tuple[tuple[Path, bytes], ...]) -> Execution:
            work = temporary / "work"
            if work.exists():
                shutil.rmtree(work)
            shutil.copytree(base, work)
            overrides = {relative.as_posix(): content for relative, content in fixture_writes}
            for fixture in test.get("fixtures", []):
                source_name = fixture["source"]
                content = overrides.get(source_name)
                if content is None:
                    content = (question_root / source_name).read_bytes()
                target = _safe_output_path(work, fixture["path"])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            completed = subprocess.run(
                test["argv"],
                cwd=work,
                input=test.get("stdin", ""),
                text=True,
                capture_output=True,
                timeout=max(5.0, test.get("timeout_ms", 2000) / 1000),
                check=False,
            )
            expected_files: list[str] = []
            for expected in test.get("expected_files", []):
                output = _safe_output_path(work, expected["path"])
                if not output.is_file():
                    raise RuntimeError(f"expected output file was not created: {output}")
                expected_files.append(output.read_text(encoding="utf-8", errors="replace"))
            return Execution(
                exit_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                expected_files=tuple(expected_files),
            )

        yield run


@contextmanager
def _mips_runner(
    question_root: Path, raw: dict[str, Any]
) -> Iterator[Callable[[dict[str, Any], tuple[tuple[Path, bytes], ...]], Execution]]:
    submission = raw["submission_files"][0]
    reference = question_root / "reference" / submission
    program = assemble([SourceUnit(str(reference), reference.read_text(encoding="utf-8"))])

    def run(test: dict[str, Any], fixture_writes: tuple[tuple[Path, bytes], ...]) -> Execution:
        if fixture_writes or test.get("fixtures") or test.get("expected_files"):
            raise RuntimeError("MIPS authoring cases may not use file fixtures")
        machine = Machine(
            program,
            argv=tuple(test["argv"][2:]),
            input_data=test.get("stdin", "").encode(),
        )
        return Execution(
            exit_code=machine.run(),
            stdout=machine.io.output.decode(),
            stderr="",
            expected_files=(),
        )

    yield run


def _input_signature(test: dict[str, Any], question_root: Path) -> tuple[object, ...]:
    fixtures = tuple(
        (fixture["path"], (question_root / fixture["source"]).read_bytes())
        for fixture in test.get("fixtures", [])
        if (question_root / fixture["source"]).is_file()
    )
    return (tuple(test["argv"]), test.get("stdin", ""), fixtures)


def _materialise_expected(test: dict[str, Any], execution: Execution) -> None:
    test["expected_stdout"] = execution.stdout
    test["expected_stderr"] = execution.stderr
    test["expected_exit"] = execution.exit_code
    test["comparison"] = "exact"
    test.pop("selected_characters", None)
    for expected, content in zip(
        test.get("expected_files", []), execution.expected_files, strict=True
    ):
        expected.pop("source", None)
        expected["content"] = content


def _add_extended_test(manifest: Path, raw: dict[str, Any]) -> bool:
    if sum(len(group["tests"]) for group in raw["test_groups"]) >= MINIMUM_TEST_POINTS:
        return False
    if any(test["id"] == EXTRA_TEST_ID for group in raw["test_groups"] for test in group["tests"]):
        return False
    question_root = manifest.parent
    signatures = {
        _input_signature(test, question_root)
        for group in raw["test_groups"]
        for test in group["tests"]
    }
    runner_context = _mips_runner if raw["kind"] == "mips_program" else _c_runner
    diagnostics: list[str] = []
    with runner_context(question_root, raw) as run:
        for candidate_index, candidate in enumerate(_candidate_tests(question_root, raw), start=1):
            if candidate_index > 160:
                break
            try:
                execution = run(candidate.test, candidate.fixture_writes)
            except (OSError, RuntimeError, subprocess.SubprocessError, UnicodeError) as exc:
                diagnostics.append(str(exc))
                continue
            expected_exit = candidate.test.get("expected_exit", 0)
            if execution.exit_code != expected_exit:
                continue
            test = candidate.test
            _materialise_expected(test, execution)
            for relative, content in candidate.fixture_writes:
                target = question_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            if _input_signature(test, question_root) in signatures:
                continue
            raw["test_groups"][-1]["tests"].append(test)
            manifest.write_text(
                json.dumps(raw, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            return True
    detail = f" Last error: {diagnostics[-1]}" if diagnostics else ""
    raise RuntimeError(f"could not derive an extra edge test for {raw['id']}.{detail}")


def _code_block(text: str) -> str:
    value = text if text else "(empty)"
    if len(value) > 240:
        value = f"{value[:237]}..."
    return f"```text\n{value.rstrip()}\n```"


def _solution_addendum(raw: dict[str, Any]) -> str:
    first_test = raw["test_groups"][0]["tests"][0]
    command = " ".join(first_test["argv"])
    fixture_names = ", ".join(
        f"{fixture['source']} -> {fixture['path']}" for fixture in first_test.get("fixtures", [])
    )
    tags = set(raw["tags"])
    if raw["kind"] == "mips_program":
        steps = (
            "1. Decide which values must survive syscalls, and assign them to stable registers.\n"
            "2. Translate the loop or function invariant into labels and explicit branches.\n"
            "3. Put the required result in `$a0`, use the documented print syscall, "
            "and emit one newline.\n"
            "4. Check the zero/empty case separately before tracing the general case."
        )
    elif tags & {"threads", "processes", "pipes", "synchronisation"}:
        steps = (
            "1. Separate input parsing from process/thread creation so every worker "
            "receives stable data.\n"
            "2. Give each worker a disjoint unit of work and compute as much as possible locally.\n"
            "3. Transfer or merge results through the required pipe/mutex boundary, "
            "then wait or join.\n"
            "4. Print only after all results are complete, and release every descriptor "
            "and allocation."
        )
    elif tags & {"file-io", "directories", "file-metadata", "binary-data"}:
        steps = (
            "1. Validate arguments, open the resource in the required mode, and check "
            "every system call.\n"
            "2. Process one byte, record, or directory entry at a time while maintaining "
            "the stated invariant.\n"
            "3. Handle short reads, empty input, and boundary offsets before formatting "
            "the result.\n"
            "4. Close descriptors and free owned memory on both success and error paths."
        )
    elif tags & {"linked-lists", "dynamic-memory", "pointers"}:
        steps = (
            "1. Draw the empty, one-node, and general cases before changing any links.\n"
            "2. Save each pointer that will still be needed, then update or recurse using "
            "the invariant above.\n"
            "3. Make ownership explicit: every retained node stays reachable and every "
            "removed allocation is freed once.\n"
            "4. Return the possibly changed head and test the boundary cases before longer lists."
        )
    else:
        steps = (
            "1. Parse the input exactly once and write down the state maintained by the "
            "main loop.\n"
            "2. Update that state for one element, character, or record at a time.\n"
            "3. Treat the smallest legal input and every equality boundary explicitly.\n"
            "4. Emit exactly the requested text and verify the final newline and spacing."
        )
    fixture_line = f"\nThe test installs `{fixture_names}` before running." if fixture_names else ""
    return (
        "\n## Step-by-step\n\n"
        f"{steps}\n\n"
        "## Worked example\n\n"
        f"The first public test, `{first_test['id']}`, runs `{command}`.{fixture_line}\n\n"
        "Input:\n\n"
        f"{_code_block(first_test.get('stdin', ''))}\n\n"
        "Expected standard output:\n\n"
        f"{_code_block(first_test.get('expected_stdout', ''))}\n\n"
        "Trace this case using the state described in **Approach**: initialise it from the first "
        "valid item, update it once per remaining item, then format the final state. The other "
        "tests deliberately cover a different boundary, so do not special-case this example.\n"
    )


def _enhance_solution(manifest: Path, raw: dict[str, Any]) -> bool:
    solution = manifest.parent / raw["solution"]
    text = solution.read_text(encoding="utf-8")
    if "## Step-by-step" in text and "## Worked example" in text:
        return False
    marker = "## Correctness"
    addendum = _solution_addendum(raw)
    if marker in text:
        text = text.replace(marker, f"{addendum}\n{marker}", 1)
    else:
        text = f"{text.rstrip()}\n{addendum}"
    solution.write_text(f"{text.rstrip()}\n", encoding="utf-8")
    return True


def upgrade_existing(*, dry_run: bool) -> tuple[int, int]:
    tests_added = 0
    solutions_enhanced = 0
    for manifest in _question_manifests():
        raw = json.loads(manifest.read_text(encoding="utf-8"))
        if dry_run:
            needs_test = (
                sum(len(group["tests"]) for group in raw["test_groups"])
                < MINIMUM_TEST_POINTS
            )
            solution_text = (manifest.parent / raw["solution"]).read_text(encoding="utf-8")
            tests_added += int(needs_test)
            solutions_enhanced += int(
                "## Step-by-step" not in solution_text or "## Worked example" not in solution_text
            )
            continue
        tests_added += int(_add_extended_test(manifest, raw))
        raw = json.loads(manifest.read_text(encoding="utf-8"))
        solutions_enhanced += int(_enhance_solution(manifest, raw))
        print(f"upgraded {raw['id']}")
    return tests_added, solutions_enhanced


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    tests_added, solutions_enhanced = upgrade_existing(dry_run=args.dry_run)
    action = "would add" if args.dry_run else "added"
    print(
        f"{action} {tests_added} edge tests; "
        f"{'would enhance' if args.dry_run else 'enhanced'} {solutions_enhanced} solutions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
