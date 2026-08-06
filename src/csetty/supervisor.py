from __future__ import annotations

import argparse
import difflib
import hashlib
import math
import os
import shlex
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Any

from .bridge import BridgeServer
from .clock import Clock, DeadlineCountdown, SystemClock, to_iso
from .docker_runtime import DockerRuntime
from .errors import CSETTYError, StateError, ValidationError
from .grading import calculate_grade, render_grade_text
from .models import Attempt, AttemptMode, AttemptState, ResultClass, TestVisibility
from .pack import Pack, Question, TestGroup, load_pack, pack_digest
from .paths import AppPaths
from .report import open_report_in_browser, report_document, write_reports
from .storage import Store, process_is_alive
from .util import canonical_json, safe_relative_path, sha256_bytes

_GREEN = "\x1b[32m"
_RED = "\x1b[31m"
_RESET = "\x1b[0m"
_DEADLINE_WARNING_THRESHOLDS = (3600, 1800, 900, 300)
_SUPERVISOR_START_TIMEOUT_SECONDS = 30.0


def _question_alias(pack: Pack, question: Question) -> str:
    for index, candidate in enumerate(pack.questions, start=1):
        if candidate.id == question.id:
            return f"q{index}"
    raise ValidationError(f"question is not part of this pack: {question.id}")


def _resolve_question(pack: Pack, activity: object) -> Question:
    question_id = str(activity)
    for question in pack.questions:
        if question.id == question_id:
            return question
    if question_id.startswith("q") and question_id[1:].isdigit():
        index = int(question_id[1:])
        if 1 <= index <= len(pack.questions):
            return pack.questions[index - 1]
    raise ValidationError(f"unknown activity: {question_id}")


def _deadline_warning_thresholds(attempt: Attempt) -> tuple[int, ...]:
    """Return only thresholds that existed when this working period began."""
    if attempt.working_started_at is None or attempt.deadline_at is None:
        return ()
    initial_seconds = math.ceil(
        max(0.0, (attempt.deadline_at - attempt.working_started_at).total_seconds())
    )
    return tuple(
        threshold for threshold in _DEADLINE_WARNING_THRESHOLDS if threshold <= initial_seconds
    )


def _remaining(seconds: int | None) -> str:
    if seconds is None:
        return "untimed"
    seconds = max(0, seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def _styled(value: str, colour: str, *, enabled: bool) -> str:
    return f"{colour}{value}{_RESET}" if enabled else value


def _result_label(result: str) -> str:
    labels = {
        ResultClass.COMPILE_ERROR.value: "compilation error",
        ResultClass.WRONG_OUTPUT.value: "incorrect output",
        ResultClass.WRONG_EXIT_STATUS.value: "incorrect exit status",
        ResultClass.RUNTIME_ERROR.value: "runtime error",
        ResultClass.TIMEOUT.value: "timeout",
        ResultClass.OUTPUT_LIMIT.value: "output limit exceeded",
        ResultClass.INTERNAL_ERROR.value: "simulator error",
    }
    return labels.get(result, result.lower().replace("_", " "))


def _output_block(lines: list[str], heading: str, value: str) -> None:
    lines.extend(("", heading, value if value else "<no output>"))


def _render_wrong_output(lines: list[str], test: Mapping[str, Any]) -> None:
    stream = "stderr" if str(test.get("detail", "")).startswith("stderr") else "stdout"
    actual = str(test.get(stream, ""))
    expected_value = test.get(f"expected_{stream}")
    expected = "" if expected_value is None else str(expected_value)
    _output_block(lines, f"Your program wrote this to {stream}:", actual)
    _output_block(lines, f"Expected {stream}:", expected)
    difference = "".join(
        difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile="your output",
            tofile="expected output",
        )
    ).rstrip("\n")
    _output_block(lines, "Difference (- your output, + expected output):", difference)


def _render_reproduction(lines: list[str], question: Question, test: Mapping[str, Any]) -> None:
    stdin = str(test.get("stdin", ""))
    argv = [str(item) for item in test.get("argv", [])]
    lines.extend(("", "Reproduce this test in the exam terminal:"))
    if question.build_argv:
        lines.append(f"  {shlex.join(question.build_argv)}")
    command = shlex.join(argv)
    if stdin:
        command = f"printf %s {shlex.quote(stdin)} | {command}"
    lines.append(f"  {command}")


def render_autotest_output(
    *, profile: str, question: Question, result: Mapping[str, Any], colour: bool
) -> str:
    lines: list[str] = []
    if question.build_argv:
        files = " ".join(question.submission_files)
        prefix = "1511" if profile == "comp1511" else "1521"
        lines.extend((f"{prefix} c_check {files}", shlex.join(question.build_argv)))

    tests = [test for group in result.get("groups", []) for test in group.get("tests", [])]
    build = result.get("build")
    if isinstance(build, dict) and result.get("status") in {
        ResultClass.COMPILE_ERROR.value,
        ResultClass.TIMEOUT.value,
        ResultClass.OUTPUT_LIMIT.value,
        ResultClass.INTERNAL_ERROR.value,
    }:
        label = _result_label(str(result["status"]))
        lines.append(_styled(f"Compilation - failed ({label})", _RED, enabled=colour))
        diagnostic = str(build.get("stderr") or build.get("stdout") or "")
        if diagnostic:
            _output_block(lines, "Compiler diagnostic:", diagnostic)
        lines.append(f"0 tests passed {len(tests)} tests failed")
        return "\n".join(lines) + "\n"

    duplicate_ids = {
        test_id
        for test_id in {str(test.get("id", "")) for test in tests}
        if sum(str(item.get("id", "")) == test_id for item in tests) > 1
    }
    passed = 0
    failed = 0
    for group in result.get("groups", []):
        for test in group.get("tests", []):
            test_id = str(test.get("id", "unnamed"))
            display_id = f"{group.get('id')}/{test_id}" if test_id in duplicate_ids else test_id
            command = shlex.join(str(item) for item in test.get("argv", []))
            result_class = str(test.get("result", ResultClass.INTERNAL_ERROR.value))
            if result_class == ResultClass.PASS.value:
                passed += 1
                status = _styled("passed", _GREEN, enabled=colour)
                lines.append(f"Test {display_id} ({command}) - {status}")
                continue
            failed += 1
            label = _result_label(result_class)
            status = _styled(f"failed ({label})", _RED, enabled=colour)
            lines.append(f"Test {display_id} ({command}) - {status}")
            detail = str(test.get("detail", ""))
            if result_class == ResultClass.WRONG_OUTPUT.value and detail.startswith(
                ("stdout", "stderr")
            ):
                _render_wrong_output(lines, test)
            else:
                if detail:
                    lines.append(detail)
                stderr = str(test.get("stderr", ""))
                if stderr:
                    _output_block(lines, "Diagnostic output:", stderr)
            stdin = str(test.get("stdin", ""))
            if stdin:
                _output_block(lines, "Input used by this test:", stdin)
            if result_class != ResultClass.INTERNAL_ERROR.value:
                _render_reproduction(lines, question, test)

    if not tests and result.get("error"):
        lines.append(f"Internal simulator error: {result['error']}")
    summary = f"{passed} tests passed {failed} tests failed"
    if failed == 0 and passed > 0:
        summary = _styled(summary, _GREEN, enabled=colour)
    lines.append(summary)
    return "\n".join(lines) + "\n"


class AttemptService:
    def __init__(
        self,
        *,
        store: Store,
        runtime: DockerRuntime,
        attempt: Attempt,
        pack: Pack,
        clock: Clock,
        report_opener: Callable[[Path], bool] | None = None,
    ) -> None:
        self.store = store
        self.runtime = runtime
        self.attempt_id = attempt.id
        self.pack = pack
        self.clock = clock
        self.report_opener = report_opener
        self.countdown = DeadlineCountdown(attempt.deadline_at, clock)

    def _attempt(self) -> Attempt:
        return self.store.expire_if_due(self.attempt_id, now=self.clock.now())

    def _verify_pack_integrity(self) -> None:
        attempt = self.store.get_attempt(self.attempt_id)
        if self.pack.root.resolve() != Path(attempt.pack_path).resolve():
            raise ValidationError("supervisor pack path does not match the attempt")
        if pack_digest(self.pack.root) != attempt.pack_digest:
            raise ValidationError("attempt pack snapshot changed after creation")

    def handle(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        self._verify_pack_integrity()
        operation = str(request["operation"])
        arguments = request.get("arguments", {})
        if operation == "status":
            return self.status()
        if operation == "questions":
            return self.questions()
        if operation == "submissions":
            return self.submissions(arguments.get("activity"))
        if operation == "check":
            return self.check()
        if operation == "submission":
            return self.show_submission(arguments.get("activity"))
        if operation == "fetch":
            return self.fetch(
                arguments.get("activity"),
                force=bool(arguments.get("force", False)),
                pack_name=arguments.get("pack_name"),
            )
        if operation == "submit":
            return self.submit(str(arguments.get("activity", "")), arguments.get("files", []))
        if operation == "autotest":
            return self.autotest(
                str(arguments.get("activity", "")),
                arguments.get("selector"),
                colour=bool(arguments.get("color", False)),
            )
        if operation == "finish":
            return self.finish()
        raise ValidationError(f"unsupported operation: {operation}")

    def status(self) -> Mapping[str, Any]:
        attempt = self._attempt()
        stdout = (
            f"Pack: {self.pack.id}@{self.pack.version}\n"
            f"Course: {self.pack.course}\n"
            f"Candidate: {attempt.candidate_id or 'practice user'}\n"
            f"Mode: {attempt.mode.value}\n"
            f"State: {attempt.state.value}\n"
            f"Time remaining: {_remaining(self.countdown.remaining_seconds())}\n"
            f"Deadline: {to_iso(attempt.deadline_at) or 'none'}\n"
            f"Toolchain image: {attempt.image}\n"
            "Submission destination: local simulator only\n"
        )
        return {"exit_code": 0, "stdout": stdout, "stderr": ""}

    def _question_state(self, attempt: Attempt, question: Question) -> str:
        latest = self.store.latest_submission(attempt.id, question.id)
        if latest is not None:
            try:
                current = self.runtime.read_workspace_files(attempt, question.submission_files)
                latest_by_path = {item["path"]: item["object_digest"] for item in latest["files"]}
                modified = any(
                    sha256_bytes(content) != latest_by_path.get(path)
                    for path, content in current.items()
                )
            except CSETTYError:
                modified = False
            return "SUBMITTED (unsubmitted changes)" if modified else "SUBMITTED"
        if self.store.has_test_run(attempt.id, question.id):
            return "TESTED"
        try:
            current = self.runtime.read_workspace_files(attempt, question.submission_files)
            for path, content in current.items():
                matching_starter = next(
                    (
                        starter
                        for starter in question.starter_files
                        if self.pack.starter_target(starter).as_posix() == path
                    ),
                    None,
                )
                if (
                    matching_starter is None
                    or content != self.pack.starter_source(matching_starter).read_bytes()
                ):
                    return "MODIFIED"
        except CSETTYError:
            pass
        return "NOT STARTED"

    def questions(self) -> Mapping[str, Any]:
        attempt = self._attempt()
        lines = []
        for question in self.pack.questions:
            files = ", ".join(question.submission_files)
            lines.append(
                f"{question.id:<12} {self._question_state(attempt, question):<30} "
                f"{question.points} points  [{files}]"
            )
        return {"exit_code": 0, "stdout": "\n".join(lines) + "\n", "stderr": ""}

    def submissions(self, activity: object) -> Mapping[str, Any]:
        question_id = None
        if activity not in {None, ""}:
            question_id = _resolve_question(self.pack, activity).id
        items = self.store.list_submissions(self.attempt_id, question_id)
        if not items:
            return {"exit_code": 0, "stdout": "No accepted local submissions.\n", "stderr": ""}
        latest_by_question: dict[str, int] = {}
        for item in items:
            latest_by_question[item["question_id"]] = max(
                latest_by_question.get(item["question_id"], 0), int(item["sequence"])
            )
        lines = ["Local simulator submissions (not sent to UNSW):"]
        for item in items:
            latest = (
                " latest" if latest_by_question[item["question_id"]] == item["sequence"] else ""
            )
            lines.append(
                f"{item['question_id']} #{item['sequence']}{latest} "
                f"{item['created_at']} {item['manifest_digest']}"
            )
        return {"exit_code": 0, "stdout": "\n".join(lines) + "\n", "stderr": ""}

    def check(self) -> Mapping[str, Any]:
        submitted = {
            str(item["question_id"]) for item in self.store.list_submissions(self.attempt_id)
        }
        labels = [
            _question_alias(self.pack, question)
            for question in self.pack.questions
            if question.id in submitted
        ]
        listing = " ".join(labels) if labels else "(none)"
        return {
            "exit_code": 0,
            "stdout": f"You have submissions for following questions:\n{listing}\n",
            "stderr": "",
        }

    def show_submission(self, activity: object) -> Mapping[str, Any]:
        question = _resolve_question(self.pack, activity)
        alias = _question_alias(self.pack, question)
        submission = self.store.latest_submission(self.attempt_id, question.id)
        if submission is None:
            return {
                "exit_code": 1,
                "stdout": "",
                "stderr": f"No submission found for {alias}.\n",
            }

        candidate = self._attempt().candidate_id or "practice user"
        rendered = [
            f"Submission for {alias}",
            f"Submitted by: {candidate}",
            f"Submitted at: {submission['created_at']}",
        ]
        for file_item in submission["files"]:
            content = self.store.object_bytes(str(file_item["object_digest"]))
            source_lines = content.decode("utf-8", errors="replace").splitlines()
            if not source_lines:
                source_lines = [""]
            width = max(4, len(str(len(source_lines))))
            rendered.extend(("", f"File: {file_item['path']}"))
            rendered.extend(
                f"{line_number:>{width}}  {line}"
                for line_number, line in enumerate(source_lines, start=1)
            )
        return {"exit_code": 0, "stdout": "\n".join(rendered) + "\n", "stderr": ""}

    def _require_working(self) -> Attempt:
        attempt = self._attempt()
        if attempt.state is not AttemptState.WORKING:
            raise StateError(f"operation is unavailable while attempt is {attempt.state.value}")
        return attempt

    def fetch(
        self, activity: object, *, force: bool, pack_name: object = None
    ) -> Mapping[str, Any]:
        attempt = self._require_working()
        if pack_name not in {None, "", self.pack.id, f"{self.pack.id}@{self.pack.version}"}:
            raise ValidationError(f"fetch pack does not match this attempt: {pack_name}")
        if force and attempt.mode is AttemptMode.EXAM:
            raise StateError("--force starter recovery is only available in practice mode")
        questions = (
            self.pack.questions
            if activity in {None, ""}
            else (_resolve_question(self.pack, activity),)
        )
        lines = []
        for question in questions:
            for starter in question.starter_files:
                target = self.pack.starter_target(starter).as_posix()
                status = self.runtime.write_workspace_file(
                    attempt,
                    target,
                    self.pack.starter_source(starter).read_bytes(),
                    overwrite=force,
                )
                lines.append(f"{target}: {status}")
        return {"exit_code": 0, "stdout": "\n".join(lines) + "\n", "stderr": ""}

    def submit(self, activity: str, explicit_files: object) -> Mapping[str, Any]:
        attempt = self._require_working()
        question = _resolve_question(self.pack, activity)
        if not isinstance(explicit_files, list) or not all(
            isinstance(item, str) for item in explicit_files
        ):
            raise ValidationError("submission files must be a list of paths")
        files = tuple(explicit_files) if explicit_files else question.submission_files
        if set(files) != set(question.submission_files) or len(files) != len(
            question.submission_files
        ):
            expected = " ".join(question.submission_files)
            raise ValidationError(f"submission files must exactly match the manifest: {expected}")
        contents = self.runtime.read_workspace_files(attempt, files)
        self.store.record_submission(
            attempt_id=attempt.id,
            question_id=question.id,
            files=contents,
            created_at=self.clock.now(),
        )
        return {
            "exit_code": 0,
            "stdout": (
                f"Your answer ({', '.join(files)}) for "
                f"{_question_alias(self.pack, question)} has been submitted.\n"
            ),
            "stderr": "",
        }

    @staticmethod
    def _selected_groups(question: Question, selector: object) -> tuple[TestGroup, ...]:
        public = tuple(
            group for group in question.test_groups if group.visibility is TestVisibility.PUBLIC
        )
        if selector in {None, ""}:
            return public
        selected = str(selector)
        by_group = tuple(group for group in public if group.id == selected)
        if by_group:
            return by_group
        for group in public:
            tests = tuple(test for test in group.tests if test.id == selected)
            if tests:
                return (replace(group, tests=tests),)
        raise ValidationError(f"public test selector not found: {selected}")

    @staticmethod
    def _snapshot_digest(files: Mapping[str, bytes]) -> str:
        manifest = [
            {"path": path, "sha256": hashlib.sha256(content).hexdigest(), "size": len(content)}
            for path, content in sorted(files.items())
        ]
        return hashlib.sha256(canonical_json(manifest)).hexdigest()

    @staticmethod
    def _materialize_files(files: Mapping[str, bytes], root: Path) -> None:
        for relative, content in files.items():
            safe = safe_relative_path(relative)
            target = root.joinpath(*safe.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)

    def autotest(
        self, activity: str, selector: object, *, colour: bool = False
    ) -> Mapping[str, Any]:
        attempt = self._require_working()
        question = _resolve_question(self.pack, activity)
        groups = self._selected_groups(question, selector)
        files = self.runtime.read_workspace_files(attempt, question.submission_files)
        snapshot_digest = self._snapshot_digest(files)
        with tempfile.TemporaryDirectory(prefix="csetty-autotest-") as temporary:
            snapshot = Path(temporary)
            self._materialize_files(files, snapshot)
            result = self.runtime.run_judge(
                attempt=attempt,
                pack=self.pack,
                question=question,
                snapshot=snapshot,
                groups=groups,
            )
        self.store.record_test_run(
            attempt_id=attempt.id,
            question_id=question.id,
            visibility="public",
            snapshot_digest=snapshot_digest,
            status=result["status"],
            created_at=self.clock.now(),
            result=result,
        )
        internal = result["status"] == "INTERNAL_ERROR"
        failed = any(
            test["result"] != ResultClass.PASS.value
            for group in result.get("groups", [])
            for test in group["tests"]
        )
        return {
            "exit_code": 5 if internal else (1 if failed else 0),
            "stdout": render_autotest_output(
                profile=attempt.profile,
                question=question,
                result=result,
                colour=colour,
            ),
            "stderr": "",
        }

    def grade(self) -> dict[str, Any]:
        existing = self.store.get_grade(self.attempt_id)
        if existing is not None:
            report = existing.get("report")
            if not isinstance(report, dict):
                raise ValidationError("stored grade report is invalid")
            restored = {str(key): value for key, value in report.items()}
            self._write_report_files(self.store.get_attempt(self.attempt_id), restored)
            return restored
        self._verify_pack_integrity()
        attempt = self.store.get_attempt(self.attempt_id)
        if not attempt.state.terminal:
            raise StateError("an attempt can only be graded after it finishes or expires")
        group_results: dict[str, dict[str, list[str]]] = {}
        detailed_results: dict[str, dict[str, list[dict[str, Any]]]] = {}
        graded_submissions: dict[str, dict[str, Any]] = {}
        for question in self.pack.questions:
            submission = self.store.latest_submission(attempt.id, question.id)
            if submission is None:
                continue
            graded_submissions[question.id] = submission
            with tempfile.TemporaryDirectory(prefix="csetty-grade-") as temporary:
                snapshot = Path(temporary)
                self.store.materialize_submission(submission, snapshot)
                result = self.runtime.run_judge(
                    attempt=attempt,
                    pack=self.pack,
                    question=question,
                    snapshot=snapshot,
                    groups=question.test_groups,
                )
            group_results[question.id] = {
                group["id"]: [test["result"] for test in group["tests"]]
                for group in result.get("groups", [])
            }
            detailed_results[question.id] = {
                group["id"]: [
                    {
                        "id": test["id"],
                        "argv": test.get("argv", []),
                        "stdin": test.get("stdin", "")[:4096],
                        "expected_stdout": (
                            None
                            if test.get("expected_stdout") is None
                            else test["expected_stdout"][:4096]
                        ),
                        "expected_stderr": (
                            None
                            if test.get("expected_stderr") is None
                            else test["expected_stderr"][:4096]
                        ),
                        "expected_exit": test.get("expected_exit"),
                        "result": test["result"],
                        "duration_ms": test["duration_ms"],
                        "exit_code": test["exit_code"],
                        "detail": test["detail"],
                        "stdout_preview": test["stdout"][:4096],
                        "stderr_preview": test["stderr"][:4096],
                    }
                    for test in group["tests"]
                ]
                for group in result.get("groups", [])
            }
            self.store.record_test_run(
                attempt_id=attempt.id,
                question_id=question.id,
                visibility="final",
                snapshot_digest=submission["manifest_digest"],
                status=result["status"],
                created_at=self.clock.now(),
                result=result,
            )
        report = calculate_grade(self.pack, group_results)
        for question_report in report["questions"]:
            question_id = question_report["id"]
            submission = graded_submissions.get(question_id)
            question_report["submission"] = (
                None
                if submission is None
                else {
                    "sequence": submission["sequence"],
                    "created_at": submission["created_at"],
                    "manifest_digest": submission["manifest_digest"],
                    "files": submission["files"],
                }
            )
            for group_report in question_report["groups"]:
                group_report["tests"] = detailed_results.get(question_id, {}).get(
                    group_report["id"], []
                )
        score = report["score"]
        self.store.record_grade(
            attempt_id=attempt.id,
            created_at=self.clock.now(),
            earned=str(score["earned"]),
            available=str(score["automatically_available"]),
            total=str(score["total"]),
            report=report,
        )
        self._write_report_files(attempt, report)
        return report

    def _write_report_files(
        self, attempt: Attempt, report: Mapping[str, Any]
    ) -> tuple[Path, Path]:
        document = report_document(
            attempt=attempt,
            pack=self.pack,
            submissions=self.store.list_submissions(attempt.id),
            grade=report,
            object_reader=self.store.object_bytes,
        )
        return write_reports(self.store.paths.reports, attempt.id, document)

    def finalize_report(self) -> tuple[dict[str, Any], Path, bool | None]:
        """Grade, persist both report formats, and optionally open the HTML report."""
        report = self.grade()
        html_report = self.store.paths.reports / f"{self.attempt_id}.html"
        opened = None if self.report_opener is None else self.report_opener(html_report)
        return report, html_report, opened

    def finish(self) -> Mapping[str, Any]:
        attempt = self._require_working()
        submitted = {item["question_id"] for item in self.store.list_submissions(attempt.id)}
        missing = [question.id for question in self.pack.questions if question.id not in submitted]
        attempt = self.store.transition(
            attempt.id,
            AttemptState.FINISHED,
            at=self.clock.now(),
            finish_reason="student",
        )
        report, html_report, opened = self.finalize_report()
        prefix = ""
        if missing:
            prefix = f"Warning: no accepted submission for {', '.join(missing)}.\n"
        if opened is True:
            report_message = f"Opened local HTML report: {html_report}\n"
        elif opened is False:
            report_message = (
                f"Local HTML report: {html_report}\n"
                "The browser could not be opened automatically.\n"
            )
        else:
            report_message = f"Local HTML report: {html_report}\n"
        return {
            "exit_code": 0,
            "stdout": (
                prefix
                + "Attempt finished.\n\n"
                + render_grade_text(report)
                + "\n\n"
                + report_message
                + f"On the host, run: csetty report {attempt.id}\n"
            ),
            "stderr": "",
        }


def run_supervisor(*, state_dir: Path, attempt_id: str, poll_seconds: float = 0.1) -> int:
    paths = AppPaths.discover(state_dir)
    store = Store(paths)
    clock = SystemClock()
    attempt = store.get_attempt(attempt_id)
    pack = load_pack(attempt.pack_path)
    if pack.digest != attempt.pack_digest:
        raise ValidationError("attempt pack content changed after attempt creation")
    runtime = DockerRuntime(paths)
    service = AttemptService(
        store=store,
        runtime=runtime,
        attempt=attempt,
        pack=pack,
        clock=clock,
        report_opener=open_report_in_browser,
    )
    bridge = BridgeServer(
        root=runtime.bridge_directory(attempt.id), attempt=attempt, store=store, clock=clock
    )
    stopping = False

    def stop(_signum: int, _frame: object) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    pid = os.getpid()
    next_warning_check = 0.0
    try:
        while not stopping:
            store.update_lease(attempt_id=attempt.id, pid=pid, at=clock.now())
            current = store.expire_if_due(attempt.id, now=clock.now())
            if current.state is AttemptState.EXPIRED:
                try:
                    _report, html_report, opened = service.finalize_report()
                    action = "Opened" if opened else "Created"
                    print(f"{action} final HTML report: {html_report}", flush=True)
                finally:
                    runtime.stop_container(current)
                return 0
            monotonic_now = clock.monotonic()
            if (
                current.state is AttemptState.WORKING
                and current.deadline_at is not None
                and monotonic_now >= next_warning_check
            ):
                remaining_seconds = service.countdown.remaining_seconds()
                assert remaining_seconds is not None
                warning_thresholds = _deadline_warning_thresholds(current)
                threshold = store.pending_deadline_warning(
                    current.id,
                    remaining_seconds=remaining_seconds,
                    thresholds=warning_thresholds,
                )
                if threshold is not None:
                    minutes = threshold // 60
                    message = f"*** CSEExamTTY EXAM TIME WARNING: {minutes} minutes remaining ***"
                    if runtime.broadcast_terminal(current, message) > 0:
                        store.record_deadline_warning(
                            current.id,
                            selected_threshold=threshold,
                            remaining_seconds=remaining_seconds,
                            thresholds=warning_thresholds,
                            at=clock.now(),
                        )
                next_warning_check = monotonic_now + 1.0
            handled = bridge.process_once(service.handle)
            current = store.get_attempt(attempt.id)
            if current.state.terminal:
                if current.state is AttemptState.EXPIRED:
                    _report, html_report, opened = service.finalize_report()
                    action = "Opened" if opened else "Created"
                    print(f"{action} final HTML report: {html_report}", flush=True)
                if handled:
                    time.sleep(0.3)
                runtime.stop_container(current)
                return 0
            time.sleep(poll_seconds)
        return 0
    finally:
        store.remove_lease(attempt.id, pid=pid)


def ensure_supervisor(paths: AppPaths, attempt: Attempt) -> int:
    store = Store(paths)
    lease = store.lease(attempt.id)
    if lease is not None and process_is_alive(int(lease["pid"])):
        return int(lease["pid"])
    log_path = paths.attempts / attempt.id / "supervisor.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log = log_path.open("ab", buffering=0)
    source_root = str(Path(__file__).resolve().parents[1])
    environment = os.environ.copy()
    current_pythonpath = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = os.pathsep.join(
        item for item in (source_root, current_pythonpath) if item
    )
    kwargs: dict[str, Any] = {
        "stdin": subprocess.DEVNULL,
        "stdout": log,
        "stderr": log,
        "cwd": str(paths.root),
        "env": environment,
        "close_fds": True,
    }
    if os.name == "nt":
        create_new_process_group = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
        detached_process = getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
        kwargs["creationflags"] = create_new_process_group | detached_process
    else:
        kwargs["start_new_session"] = True
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "csetty.supervisor",
            "--state-dir",
            str(paths.root),
            "--attempt",
            attempt.id,
        ],
        **kwargs,
    )
    log.close()
    deadline = time.monotonic() + _SUPERVISOR_START_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        lease = store.lease(attempt.id)
        if lease is not None and int(lease["pid"]) == process.pid:
            return process.pid
        if process.poll() is not None:
            detail = log_path.read_text(encoding="utf-8", errors="replace")
            raise CSETTYError(f"supervisor failed to start: {detail.strip()}")
        time.sleep(0.05)
    # Check once more at the boundary before terminating a process that became
    # healthy during the final scheduler interval.
    lease = store.lease(attempt.id)
    if lease is not None and int(lease["pid"]) == process.pid:
        return process.pid
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    detail = log_path.read_text(encoding="utf-8", errors="replace").strip()
    suffix = f"; inspect {log_path}: {detail}" if detail else f"; inspect {log_path}"
    raise CSETTYError(
        "supervisor did not publish a lease within "
        f"{_SUPERVISOR_START_TIMEOUT_SECONDS:g} seconds{suffix}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="csetty-supervisor")
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--attempt", required=True)
    args = parser.parse_args(argv)
    try:
        return run_supervisor(state_dir=args.state_dir, attempt_id=args.attempt)
    except CSETTYError as exc:
        print(exc.message, file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
