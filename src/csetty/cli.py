from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
import uuid
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path

from csetty_mips import __version__ as CSETTY_MIPS_VERSION

from . import __version__
from .clock import SystemClock
from .companion import launch_companion
from .docker_runtime import DockerRuntime
from .errors import CSETTYError, StateError, ToolUnavailableError, UsageError, ValidationError
from .exam_gate import run_exam_entry_gate
from .models import Attempt, AttemptMode, AttemptState, WorkspaceKind
from .pack import Pack, PackRepository, load_pack, snapshot_author_materials, snapshot_pack
from .paths import AppPaths
from .question_bank import build_exam_pack, build_verification_pack, load_question_bank
from .report import open_report_in_browser, render_report_text
from .storage import Store
from .supervisor import AttemptService, ensure_supervisor
from .util import atomic_write
from .vscode import VSCodeManager


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="csetty", description="Local CSE exam workflow simulator")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor = subcommands.add_parser("doctor", help="check the host environment")
    doctor.add_argument("--offline-ready", choices=("comp1511", "comp1521"))

    prepare = subcommands.add_parser("prepare", help="prepare images and isolated VS Code caches")
    prepare.add_argument("--profile", choices=("comp1511", "comp1521", "all"), required=True)
    prepare.add_argument(
        "--mipsy-source",
        type=Path,
        help="optionally validate and record the pinned private upstream comparison checkout",
    )

    packs = subcommands.add_parser("packs", help="manage installed packs")
    packs_sub = packs.add_subparsers(dest="packs_command", required=True)
    packs_sub.add_parser("list", help="list installed packs")

    pack = subcommands.add_parser("pack", help="validate or verify a pack")
    pack_sub = pack.add_subparsers(dest="pack_command", required=True)
    validate = pack_sub.add_parser("validate")
    validate.add_argument("path", type=Path)
    verify = pack_sub.add_parser("verify")
    verify.add_argument("path", type=Path)
    verify.add_argument("--reference", type=Path, required=True)

    start = subcommands.add_parser("start", help="create and start an attempt")
    start.add_argument("pack")
    start.add_argument("--mode", choices=("practice", "exam"), default="practice")
    start.add_argument("--editor", choices=("code", "terminal"), default="code")
    start.add_argument("--workspace", type=Path)
    start.add_argument("--network", choices=("none", "on"), default="none")
    start.add_argument("--timed", action="store_true")
    start.add_argument("--skip-reading", action="store_true")

    resume = subcommands.add_parser("resume", help="resume an active attempt")
    resume.add_argument("attempt_id", nargs="?")

    code = subcommands.add_parser("code", help="open the exam container in isolated VS Code")
    code.add_argument("attempt_id", nargs="?")

    page = subcommands.add_parser("page", help="open the local exam companion page")
    page.add_argument("attempt_id", nargs="?")

    export = subcommands.add_parser("export", help="export an attempt workspace")
    export.add_argument("attempt_id")
    export.add_argument("destination", type=Path)

    attempts = subcommands.add_parser("attempts", help="list attempts")
    attempts_sub = attempts.add_subparsers(dest="attempts_command", required=True)
    attempts_sub.add_parser("list")

    report = subcommands.add_parser("report", help="show an attempt report")
    report.add_argument("attempt_id", nargs="?")
    report.add_argument("--json", action="store_true")

    bank = subcommands.add_parser("bank", help="validate and build from original question banks")
    bank_sub = bank.add_subparsers(dest="bank_command", required=True)
    bank_validate = bank_sub.add_parser("validate", help="validate a question bank")
    bank_validate.add_argument("path", type=Path)
    bank_stats = bank_sub.add_parser("stats", help="show question-bank coverage")
    bank_stats.add_argument("path", type=Path)
    bank_verify = bank_sub.add_parser(
        "verify", help="run every question's reference solution in the isolated judge"
    )
    bank_verify.add_argument("path", type=Path)
    bank_build = bank_sub.add_parser("build", help="build a deterministic original exam pack")
    bank_build.add_argument("path", type=Path)
    bank_build.add_argument("destination", type=Path)
    bank_build.add_argument("--seed", type=int, required=True)
    bank_build.add_argument("--version", default="1.0.0")
    return parser


def _components(
    state_dir: Path | None = None,
) -> tuple[AppPaths, Store, DockerRuntime, VSCodeManager]:
    paths = AppPaths.discover(state_dir)
    paths.ensure()
    store = Store(paths)
    runtime = DockerRuntime(paths)
    vscode = VSCodeManager(paths, runtime)
    return paths, store, runtime, vscode


def _doctor(args: argparse.Namespace) -> int:
    paths, _store, runtime, vscode = _components()
    docker = runtime.doctor()
    checks: list[tuple[str, bool, str]] = [
        ("Python >= 3.11", sys.version_info >= (3, 11), sys.version.split()[0]),
        ("State directory", os.access(paths.root, os.W_OK), str(paths.root)),
        ("Docker CLI", bool(docker["cli"]), str(docker["cli_version"])),
        (
            "Docker daemon",
            bool(docker["daemon"]),
            str(docker["server_version"] or docker["error"]),
        ),
    ]
    try:
        version = vscode.version()
        checks.append(("VS Code CLI", True, f"{version['version']} ({version['commit']})"))
    except CSETTYError as exc:
        checks.append(("VS Code CLI", False, exc.message))
    try:
        pack_count = len(PackRepository().list())
        checks.append(("Installed packs", pack_count > 0, str(pack_count)))
    except CSETTYError as exc:
        checks.append(("Installed packs", False, exc.message))
    if args.offline_ready:
        try:
            runtime.ensure_profile_ready(args.offline_ready)
            image_ready, image_detail = True, "interactive and judge image IDs verified"
        except CSETTYError as exc:
            image_ready, image_detail = False, exc.message
        checks.append((f"Local images ({args.offline_ready})", image_ready, image_detail))
        try:
            ready, detail = vscode.offline_ready(args.offline_ready)
        except CSETTYError as exc:
            ready, detail = False, exc.message
        checks.append((f"Offline VS Code ({args.offline_ready})", ready, detail))
    for label, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'}  {label}: {detail}")
    return 0 if all(passed for _label, passed, _detail in checks) else 4


def _prepare(args: argparse.Namespace) -> int:
    paths, _store, runtime, vscode = _components()
    profiles = ("comp1511", "comp1521") if args.profile == "all" else (args.profile,)
    mipsy_source = args.mipsy_source
    if mipsy_source is not None and "comp1521" not in profiles:
        raise UsageError("--mipsy-source is only valid when preparing COMP1521 or all profiles")
    mips_record: dict[str, object] = {
        "schema_version": 2,
        "course_engine": {
            "name": "csetty-mips",
            "version": CSETTY_MIPS_VERSION,
            "bundled": True,
        },
        "upstream_oracle": None,
    }
    if mipsy_source is not None:
        source = mipsy_source.expanduser().resolve()
        actual_commit = runtime.validate_mipsy_oracle_source(source)
        mips_record["upstream_oracle"] = {
            "source": str(source),
            "commit": actual_commit,
            "redistributable": False,
            "purpose": "private-black-box-comparison-only",
            "used_in_course_image": False,
        }
        print(
            "Validated pinned upstream source as a private comparison oracle; "
            "the course image still uses csetty-mips."
        )
    if "comp1521" in profiles:
        atomic_write(
            paths.cache / "mipsy.json",
            (json.dumps(mips_record, indent=2, sort_keys=True) + "\n").encode(),
        )
    for profile in profiles:
        print(f"Building {profile} interactive and judge images from source...")
        runtime.build_image(profile)
        print(f"Preparing isolated VS Code profile for {profile}...")
        readiness = vscode.prepare(profile)
        print(f"Prepared {profile}: VS Code {readiness['code']['version']}")
    return 0


def _list_packs() -> int:
    packs = PackRepository().list()
    if not packs:
        print("No exam packs are installed.")
        return 0
    for pack in packs:
        print(
            f"{pack.id}@{pack.version}\t{pack.course}\t{len(pack.questions)} questions\t"
            f"{pack.total_points} points\t{pack.title}"
        )
    return 0


def _validate_pack(path: Path) -> int:
    pack = load_pack(path)
    print(f"Valid: {pack.id}@{pack.version}")
    print(f"Digest: {pack.digest}")
    print(f"Questions: {len(pack.questions)}; points: {pack.total_points}")
    for warning in pack.warnings:
        print(f"Warning: {warning}")
    return 0


def _reference_files(pack: Pack, question_id: str, root: Path) -> dict[str, Path]:
    question = pack.question(question_id)
    result = {}
    for relative in question.submission_files:
        candidate = root.joinpath(*Path(relative).parts)
        if not candidate.is_file() or candidate.is_symlink():
            raise ValidationError(f"reference solution is missing {relative} for {question_id}")
        result[relative] = candidate
    return result


def _verify_pack(path: Path, reference: Path) -> int:
    pack = load_pack(path)
    paths, _store, runtime, _vscode = _components()
    image = runtime.image_for_profile(pack.profile)
    runtime.ensure_profile_ready(pack.profile)
    now = SystemClock().now()
    dummy = Attempt(
        id="pack-verification",
        pack_id=pack.id,
        pack_version=pack.version,
        pack_path=str(pack.root),
        pack_digest=pack.digest,
        course=pack.course,
        profile=pack.profile,
        mode=AttemptMode.PRACTICE,
        state=AttemptState.FINISHED,
        timed=False,
        created_at=now,
        reading_started_at=None,
        working_started_at=None,
        deadline_at=None,
        finished_at=now,
        finish_reason="verification",
        workspace_kind=WorkspaceKind.BIND,
        workspace_ref="",
        image=image,
        provenance={},
        container_name="",
        session_token="",
        network="none",
        editor="terminal",
    )
    failures = 0
    for question in pack.questions:
        with tempfile.TemporaryDirectory(prefix="csetty-reference-") as temporary:
            snapshot = Path(temporary)
            for relative, source in _reference_files(pack, question.id, reference).items():
                target = snapshot / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            result = runtime.run_judge(
                attempt=dummy,
                pack=pack,
                question=question,
                snapshot=snapshot,
                groups=question.test_groups,
            )
        passed = all(
            test["result"] == "PASS"
            for group in result.get("groups", [])
            for test in group["tests"]
        )
        failures += not passed
        print(f"{'PASS' if passed else 'FAIL'}  {question.id}")
        if not passed:
            if result.get("error"):
                print(f"  judge: {result['error']}")
            for group in result.get("groups", []):
                for test in group["tests"]:
                    if test["result"] == "PASS":
                        continue
                    print(
                        f"  {group['id']}/{test['id']}: {test['result']} ({test.get('detail', '')})"
                    )
                    if test.get("stdout"):
                        print(f"    stdout: {test['stdout'][:500]!r}")
                    if test.get("stderr"):
                        print(f"    stderr: {test['stderr'][:500]!r}")
    if failures:
        raise ValidationError(f"reference verification failed for {failures} question(s)")
    print(f"Reference solution passed all tests for {pack.id}@{pack.version}")
    return 0


def _check_start_options(args: argparse.Namespace) -> tuple[AttemptMode, bool, str]:
    mode = AttemptMode(args.mode)
    timed = mode is AttemptMode.EXAM or bool(args.timed)
    if mode is AttemptMode.EXAM and args.network == "on":
        raise UsageError("exam mode requires --network none")
    if mode is AttemptMode.EXAM and args.skip_reading:
        raise UsageError("exam mode does not allow --skip-reading")
    network = "bridge" if args.network == "on" else "none"
    return mode, timed, network


def _reading(pack: Pack, *, ends_at: datetime, clock: SystemClock) -> None:
    print(pack.paper_text())
    if pack.resources:
        print("\nPermitted resources:")
        for resource in pack.resources:
            print(f"  {resource.label}: {resource.path}")
    print("\nReading time is read-only. The workspace and editor have not started.")
    monotonic_end = clock.monotonic() + max(0.0, (ends_at - clock.now()).total_seconds())
    try:
        while clock.monotonic() < monotonic_end:
            remaining = max(0, int(monotonic_end - clock.monotonic()))
            minutes, seconds = divmod(remaining, 60)
            print(f"\rReading time remaining: {minutes:02d}:{seconds:02d}", end="", flush=True)
            time.sleep(min(1, max(0.05, monotonic_end - clock.monotonic())))
    except KeyboardInterrupt:
        print("\nReading view closed. The clock continues; run csetty resume to continue.")
        raise StateError("attempt remains in reading time") from None
    print("\rReading time complete.                    ")


def _ensure_editor_ready(attempt: Attempt, vscode: VSCodeManager) -> None:
    if attempt.editor != "code":
        return
    ready, detail = vscode.offline_ready(attempt.profile)
    if not ready:
        raise ToolUnavailableError(detail)


def _attempt_pack(attempt: Attempt) -> Pack:
    pack = load_pack(attempt.pack_path)
    if pack.digest != attempt.pack_digest:
        raise ValidationError("attempt pack content changed after attempt creation")
    return pack


def _launch_working(
    *,
    attempt: Attempt,
    pack: Pack,
    paths: AppPaths,
    store: Store,
    runtime: DockerRuntime,
    vscode: VSCodeManager,
    open_companion_browser: bool = True,
) -> int:
    clock = SystemClock()
    attempt = store.expire_if_due(attempt.id, now=clock.now())
    if attempt.state is AttemptState.EXPIRED:
        try:
            service = AttemptService(
                store=store,
                runtime=runtime,
                attempt=attempt,
                pack=pack,
                clock=clock,
                report_opener=open_report_in_browser,
            )
            _report, html_report, opened = service.finalize_report()
        finally:
            runtime.stop_container(attempt)
        if opened:
            raise StateError("attempt deadline has passed; the final report was opened")
        raise StateError(f"attempt deadline has passed; final report: {html_report}")
    if attempt.state is not AttemptState.WORKING:
        raise StateError(f"cannot launch workspace while attempt is {attempt.state.value}")
    _ensure_editor_ready(attempt, vscode)
    runtime.start_container(attempt, pack, network=attempt.network)
    ensure_supervisor(paths, attempt)
    companion = launch_companion(paths, attempt, open_browser=open_companion_browser)
    if open_companion_browser:
        print(f"Exam companion page is ready (browser launch requested): {companion.url}")
    else:
        print(f"Exam companion page is ready: {companion.url}")
    if attempt.editor == "code":
        vscode.attach(attempt)
        print(f"Opened isolated VS Code for attempt {attempt.id}")
        print("The attempt clock continues when the VS Code window is closed.")
        return 0
    return runtime.attach_terminal(attempt)


def _enter_working(
    *,
    attempt: Attempt,
    pack: Pack,
    store: Store,
    anchor: datetime,
) -> Attempt:
    clock = SystemClock()
    deadline = anchor + timedelta(seconds=pack.working_time_seconds) if attempt.timed else None
    working = store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=clock.now(),
        deadline_at=deadline,
    )
    return store.expire_if_due(working.id, now=clock.now())


def _start(args: argparse.Namespace) -> int:
    mode, timed, network = _check_start_options(args)
    pack = PackRepository().get(args.pack)
    paths, store, runtime, vscode = _components()
    image = runtime.image_for_profile(pack.profile)
    runtime.ensure_profile_ready(pack.profile)
    if args.editor == "code":
        ready, detail = vscode.offline_ready(pack.profile)
        if not ready:
            raise ToolUnavailableError(detail)

    candidate_id = None
    if mode is AttemptMode.EXAM:
        candidate_id = run_exam_entry_gate(pack.course)

    if args.workspace is None:
        workspace_kind = WorkspaceKind.VOLUME
        workspace_ref = f"csetty-ws-{uuid.uuid4().hex[:16]}"
    else:
        workspace_kind = WorkspaceKind.BIND
        workspace = args.workspace.expanduser().resolve()
        workspace.mkdir(parents=True, exist_ok=True)
        if any(item for item in workspace.iterdir() if item.name != ".DS_Store"):
            raise ValidationError("--workspace must refer to an empty directory for a new attempt")
        workspace_ref = str(workspace)

    clock = SystemClock()
    provenance = dict(runtime.profile_provenance(pack.profile))
    while True:
        attempt_id = str(uuid.uuid4())
        attempt_root = paths.attempts / attempt_id
        if not attempt_root.exists():
            break
    try:
        provenance["author_materials_digest"] = snapshot_author_materials(
            pack, attempt_root / "author"
        )
        pack = snapshot_pack(pack, attempt_root / "pack")
        attempt = store.create_attempt(
            pack_id=pack.id,
            pack_version=pack.version,
            pack_path=pack.root,
            pack_digest=pack.digest,
            course=pack.course,
            profile=pack.profile,
            mode=mode,
            timed=timed,
            created_at=clock.now(),
            workspace_kind=workspace_kind,
            workspace_ref=workspace_ref,
            image=image,
            provenance=provenance,
            network=network,
            editor=args.editor,
            candidate_id=candidate_id,
            skip_reading=bool(args.skip_reading),
            attempt_id=attempt_id,
        )
    except Exception:
        shutil.rmtree(attempt_root, ignore_errors=True)
        raise
    print(f"Attempt created: {attempt.id}")
    should_read = pack.reading_time_seconds > 0 and not attempt.skip_reading
    reading_page_open = False
    if should_read:
        def begin_reading() -> None:
            nonlocal attempt
            attempt = store.transition(attempt.id, AttemptState.READING, at=clock.now())

        companion = launch_companion(paths, attempt, ready_callback=begin_reading)
        reading_page_open = True
        print(f"Opened read-only exam paper: {companion.url}")
        assert attempt.reading_started_at is not None
        reading_end = attempt.reading_started_at + timedelta(seconds=pack.reading_time_seconds)
        _reading(pack, ends_at=reading_end, clock=clock)
        attempt = _enter_working(attempt=attempt, pack=pack, store=store, anchor=reading_end)
    else:
        attempt = _enter_working(attempt=attempt, pack=pack, store=store, anchor=clock.now())
    return _launch_working(
        attempt=attempt,
        pack=pack,
        paths=paths,
        store=store,
        runtime=runtime,
        vscode=vscode,
        open_companion_browser=not reading_page_open,
    )


def _resume(args: argparse.Namespace) -> int:
    paths, store, runtime, vscode = _components()
    clock = SystemClock()
    attempt = store.resolve_attempt(args.attempt_id)
    pack = _attempt_pack(attempt)
    if attempt.state.terminal:
        raise StateError(f"attempt is already {attempt.state.value}; use csetty report")
    if attempt.state is AttemptState.READING:
        assert attempt.reading_started_at is not None
        reading_end = attempt.reading_started_at + timedelta(seconds=pack.reading_time_seconds)
        if clock.now() < reading_end:
            companion = launch_companion(paths, attempt)
            reading_page_open = True
            print(f"Read-only exam paper is ready: {companion.url}")
            _reading(pack, ends_at=reading_end, clock=clock)
        else:
            reading_page_open = False
        attempt = _enter_working(attempt=attempt, pack=pack, store=store, anchor=reading_end)
    elif attempt.state is AttemptState.CREATED:
        if pack.reading_time_seconds > 0 and not attempt.skip_reading:
            def begin_reading() -> None:
                nonlocal attempt
                attempt = store.transition(attempt.id, AttemptState.READING, at=clock.now())

            companion = launch_companion(paths, attempt, ready_callback=begin_reading)
            reading_page_open = True
            print(f"Opened read-only exam paper: {companion.url}")
            assert attempt.reading_started_at is not None
            reading_end = attempt.reading_started_at + timedelta(
                seconds=pack.reading_time_seconds
            )
            _reading(pack, ends_at=reading_end, clock=clock)
            attempt = _enter_working(
                attempt=attempt,
                pack=pack,
                store=store,
                anchor=reading_end,
            )
        else:
            reading_page_open = False
            attempt = _enter_working(
                attempt=attempt,
                pack=pack,
                store=store,
                anchor=clock.now(),
            )
    else:
        reading_page_open = False
    return _launch_working(
        attempt=attempt,
        pack=pack,
        paths=paths,
        store=store,
        runtime=runtime,
        vscode=vscode,
        open_companion_browser=not reading_page_open,
    )


def _code(args: argparse.Namespace) -> int:
    paths, store, runtime, vscode = _components()
    attempt = store.resolve_attempt(args.attempt_id)
    if attempt.state is not AttemptState.WORKING:
        raise StateError(f"VS Code is unavailable while attempt is {attempt.state.value}")
    if attempt.editor != "code":
        raise StateError(
            "this attempt was started with --editor terminal and has no offline VS Code cache mount"
        )
    pack = _attempt_pack(attempt)
    ready, detail = vscode.offline_ready(attempt.profile)
    if not ready:
        raise ToolUnavailableError(detail)
    runtime.start_container(attempt, pack, network=attempt.network)
    ensure_supervisor(paths, attempt)
    vscode.attach(attempt)
    print(f"Opened isolated VS Code for attempt {attempt.id}")
    return 0


def _page(args: argparse.Namespace) -> int:
    paths, store, _runtime, _vscode = _components()
    attempt = store.resolve_attempt(args.attempt_id)
    companion = launch_companion(paths, attempt)
    print(f"Exam companion page is ready (browser launch requested): {companion.url}")
    return 0


def _export(args: argparse.Namespace) -> int:
    _paths, store, runtime, _vscode = _components()
    attempt = store.resolve_attempt(args.attempt_id)
    runtime.export_workspace(attempt, args.destination)
    print(f"Exported workspace to {args.destination.expanduser().resolve()}")
    return 0


def _list_attempts() -> int:
    _paths, store, _runtime, _vscode = _components()
    attempts = store.list_attempts()
    if not attempts:
        print("No attempts.")
        return 0
    for attempt in attempts:
        print(
            f"{attempt.id}\t{attempt.state.value}\t{attempt.mode.value}\t"
            f"{attempt.pack_id}@{attempt.pack_version}\t"
            f"{attempt.candidate_id or '-'}\t{attempt.created_at.isoformat()}"
        )
    return 0


def _report(args: argparse.Namespace) -> int:
    _paths, store, runtime, _vscode = _components()
    clock = SystemClock()
    if args.attempt_id is None:
        attempts = store.list_attempts()
        if not attempts:
            raise ValidationError("there is no attempt to report")
        attempt = attempts[0]
    else:
        attempt = store.resolve_attempt(args.attempt_id)
    pack = _attempt_pack(attempt)
    service = AttemptService(
        store=store, runtime=runtime, attempt=attempt, pack=pack, clock=clock
    )
    document, json_path, html_path, _finalized = service.publish_report()
    if args.json:
        print(json.dumps(document, indent=2, sort_keys=True))
    else:
        print(render_report_text(document))
        print(f"\nJSON: {json_path}")
        print(f"HTML: {html_path}")
    return 0


def _bank(args: argparse.Namespace) -> int:
    bank = load_question_bank(args.path)
    if args.bank_command == "validate":
        print(f"Valid: {bank.id}")
        print(f"Course: {bank.course}")
        print(f"Questions: {len(bank.questions)}")
        return 0
    if args.bank_command == "stats":
        print(json.dumps(bank.stats(), indent=2, sort_keys=True))
        return 0
    if args.bank_command == "verify":
        with tempfile.TemporaryDirectory(prefix=f"csetty-{bank.profile}-bank-verify-") as temporary:
            pack = build_verification_pack(bank, destination=Path(temporary))
            print(f"Verifying all {len(pack.questions)} questions in {bank.id}...")
            return _verify_pack(pack.root, pack.root / "solutions" / "reference")
    if args.bank_command == "build":
        pack = build_exam_pack(
            bank,
            destination=args.destination,
            seed=args.seed,
            version=args.version,
        )
        print(f"Built: {pack.id}@{pack.version}")
        print(f"Path: {pack.root}")
        print(f"Digest: {pack.digest}")
        return 0
    raise UsageError("unsupported bank command")


def dispatch(args: argparse.Namespace) -> int:
    if args.command == "doctor":
        return _doctor(args)
    if args.command == "prepare":
        return _prepare(args)
    if args.command == "packs" and args.packs_command == "list":
        return _list_packs()
    if args.command == "pack" and args.pack_command == "validate":
        return _validate_pack(args.path)
    if args.command == "pack" and args.pack_command == "verify":
        return _verify_pack(args.path, args.reference)
    if args.command == "start":
        return _start(args)
    if args.command == "resume":
        return _resume(args)
    if args.command == "code":
        return _code(args)
    if args.command == "page":
        return _page(args)
    if args.command == "export":
        return _export(args)
    if args.command == "attempts" and args.attempts_command == "list":
        return _list_attempts()
    if args.command == "report":
        return _report(args)
    if args.command == "bank":
        return _bank(args)
    raise UsageError("unsupported command")


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        return dispatch(args)
    except CSETTYError as exc:
        print(f"csetty: {exc.message}", file=sys.stderr)
        return exc.exit_code
    except KeyboardInterrupt:
        print("csetty: interrupted", file=sys.stderr)
        return 130
