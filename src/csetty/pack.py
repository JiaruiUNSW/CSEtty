from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import tempfile
import tomllib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any

from .assets import assets_root
from .errors import ValidationError
from .models import TestVisibility
from .util import resolve_under, safe_relative_path

_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
_VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
_COMPARISONS = {
    "exact",
    "ignore_trailing_whitespace",
    "ignore_whitespace",
    "ignore_case",
    "selected_characters",
}
_ALLOWED_EXECUTABLES = {
    "bash",
    "clang",
    "dcc",
    "gcc",
    "make",
    "mipsy",
    "python3",
    "sh",
}
_MAX_CPUS = 8.0
_MAX_MEMORY_MB = 4096
_MAX_PIDS = 512
_MAX_OUTPUT_LIMIT_KB = 2048
_MAX_TEST_TIMEOUT_MS = 60_000
_EXCLUDED_PACK_DIRECTORIES = {".git", "solutions"}


@dataclass(frozen=True)
class EnvironmentSpec:
    image: str
    network: str
    cpus: float
    memory_mb: int
    pids: int
    output_limit_kb: int


@dataclass(frozen=True)
class ResourceSpec:
    path: str
    label: str


@dataclass(frozen=True)
class FixtureSpec:
    source: str
    path: str


@dataclass(frozen=True)
class ExpectedFileSpec:
    path: str
    content: str | None
    source: str | None


@dataclass(frozen=True)
class TestCase:
    id: str
    argv: tuple[str, ...]
    stdin: str
    expected_stdout: str | None
    expected_stderr: str | None
    expected_exit: int | None
    timeout_ms: int
    comparison: str
    selected_characters: str | None
    fixtures: tuple[FixtureSpec, ...]
    expected_files: tuple[ExpectedFileSpec, ...]


@dataclass(frozen=True)
class TestGroup:
    id: str
    visibility: TestVisibility
    points: Decimal
    tests: tuple[TestCase, ...]


@dataclass(frozen=True)
class Question:
    id: str
    title: str
    kind: str
    points: Decimal
    pass_points: Decimal
    starter_files: tuple[str, ...]
    submission_files: tuple[str, ...]
    build_argv: tuple[str, ...]
    test_groups: tuple[TestGroup, ...]
    prompt: str | None = None
    difficulty: int = 3
    track: str = "normal"
    tags: tuple[str, ...] = ()
    estimated_minutes: int | None = None

    @property
    def automatic_points(self) -> Decimal:
        return sum((group.points for group in self.test_groups), Decimal(0))

    def group(self, group_id: str) -> TestGroup:
        for group in self.test_groups:
            if group.id == group_id:
                return group
        raise ValidationError(f"unknown test group {group_id!r} for {self.id}")


@dataclass(frozen=True)
class Hurdle:
    id: str
    label: str
    question_ids: tuple[str, ...]
    min_passed_questions: int


@dataclass(frozen=True)
class Pack:
    root: Path
    schema_version: int
    id: str
    version: str
    title: str
    course: str
    profile: str
    author: str
    license: str
    paper: str
    reading_time_seconds: int
    working_time_seconds: int
    environment: EnvironmentSpec
    resources: tuple[ResourceSpec, ...]
    questions: tuple[Question, ...]
    hurdles: tuple[Hurdle, ...]
    digest: str
    warnings: tuple[str, ...]

    @property
    def total_points(self) -> Decimal:
        return sum((question.points for question in self.questions), Decimal(0))

    def question(self, question_id: str) -> Question:
        for question in self.questions:
            if question.id == question_id:
                return question
        raise ValidationError(f"unknown activity: {question_id}")

    def paper_text(self) -> str:
        return resolve_under(self.root, self.paper).read_text(encoding="utf-8")

    def question_prompt(self, question: Question) -> str:
        if question.prompt is None:
            return f"# {question.title}\n\nNo extended question description is available.\n"
        return resolve_under(self.root, question.prompt).read_text(encoding="utf-8")

    def starter_source(self, starter_path: str) -> Path:
        return resolve_under(self.root, starter_path)

    @staticmethod
    def starter_target(starter_path: str) -> PurePosixPath:
        path = safe_relative_path(starter_path, label="starter path")
        if path.parts and path.parts[0] == "starter":
            path = PurePosixPath(*path.parts[1:])
        if not path.parts:
            raise ValidationError(f"starter path has no destination: {starter_path}")
        return path


def _required(
    mapping: Mapping[str, Any],
    key: str,
    expected: type[Any] | tuple[type[Any], ...],
    context: str,
) -> Any:
    if key not in mapping:
        raise ValidationError(f"{context}: missing required field {key!r}")
    value = mapping[key]
    if not isinstance(value, expected):
        expected_types = expected if isinstance(expected, tuple) else (expected,)
        expected_name = " or ".join(item.__name__ for item in expected_types)
        raise ValidationError(f"{context}.{key} must be {expected_name}")
    return value


def _decimal(value: object, *, context: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValidationError(f"{context} must be a number")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValidationError(f"{context} must be a number") from exc
    if not result.is_finite() or result < 0:
        raise ValidationError(f"{context} must be a non-negative finite number")
    return result


def _bounded_integer(value: object, *, context: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{context} must be an integer")
    if value <= 0 or value > maximum:
        raise ValidationError(f"{context} must be between 1 and {maximum}")
    return value


def _identifier(value: str, *, context: str) -> str:
    if not _ID_PATTERN.fullmatch(value):
        raise ValidationError(f"{context} must match {_ID_PATTERN.pattern}")
    return value


def _string_list(value: object, *, context: str, nonempty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, list) or (nonempty and not value):
        suffix = "non-empty " if nonempty else ""
        raise ValidationError(f"{context} must be a {suffix}list")
    if not all(isinstance(item, str) and item for item in value):
        raise ValidationError(f"{context} entries must be non-empty strings")
    return tuple(value)


def _validate_argv(value: object, *, context: str, allow_empty: bool = False) -> tuple[str, ...]:
    argv = _string_list(value, context=context, nonempty=not allow_empty)
    if not argv:
        return argv
    executable = argv[0]
    if executable not in _ALLOWED_EXECUTABLES and not executable.startswith("./"):
        raise ValidationError(f"{context}: executable {executable!r} is not allowed")
    if any("\x00" in arg for arg in argv):
        raise ValidationError(f"{context}: arguments may not contain NUL")
    return argv


def _read_expected(
    raw: Mapping[str, Any],
    *,
    inline_key: str,
    path_key: str,
    root: Path,
    context: str,
) -> str | None:
    inline = raw.get(inline_key)
    file_path = raw.get(path_key)
    if inline is not None and file_path is not None:
        raise ValidationError(f"{context}: use only one of {inline_key} and {path_key}")
    if inline is not None:
        if not isinstance(inline, str):
            raise ValidationError(f"{context}.{inline_key} must be a string")
        return inline
    if file_path is not None:
        if not isinstance(file_path, str):
            raise ValidationError(f"{context}.{path_key} must be a path string")
        return resolve_under(root, file_path).read_text(encoding="utf-8")
    return None


def _parse_test(raw: Mapping[str, Any], *, root: Path, context: str) -> TestCase:
    test_id = _identifier(_required(raw, "id", str, context), context=f"{context}.id")
    argv = _validate_argv(_required(raw, "argv", list, context), context=f"{context}.argv")
    stdin = raw.get("stdin", "")
    if not isinstance(stdin, str):
        raise ValidationError(f"{context}.stdin must be a string")
    expected_stdout = _read_expected(
        raw,
        inline_key="expected_stdout",
        path_key="expected_stdout_path",
        root=root,
        context=context,
    )
    expected_stderr = _read_expected(
        raw,
        inline_key="expected_stderr",
        path_key="expected_stderr_path",
        root=root,
        context=context,
    )
    expected_exit = raw.get("expected_exit", 0)
    if expected_exit is not None and (
        isinstance(expected_exit, bool) or not isinstance(expected_exit, int)
    ):
        raise ValidationError(f"{context}.expected_exit must be an integer or omitted")
    timeout_ms = raw.get("timeout_ms", 2000)
    timeout_ms = _bounded_integer(
        timeout_ms,
        context=f"{context}.timeout_ms",
        maximum=_MAX_TEST_TIMEOUT_MS,
    )
    comparison = raw.get("comparison", "exact")
    if comparison not in _COMPARISONS:
        raise ValidationError(f"{context}.comparison is unsupported: {comparison!r}")
    selected = raw.get("selected_characters")
    if comparison == "selected_characters" and not isinstance(selected, str):
        raise ValidationError(f"{context}.selected_characters is required")
    if selected is not None and not isinstance(selected, str):
        raise ValidationError(f"{context}.selected_characters must be a string")

    fixtures: list[FixtureSpec] = []
    for index, fixture in enumerate(raw.get("fixtures", [])):
        fixture_context = f"{context}.fixtures[{index}]"
        if not isinstance(fixture, dict):
            raise ValidationError(f"{fixture_context} must be a table")
        source = _required(fixture, "source", str, fixture_context)
        target = _required(fixture, "path", str, fixture_context)
        resolve_under(root, source)
        safe_relative_path(target, label=f"{fixture_context}.path")
        fixtures.append(FixtureSpec(source=source, path=target))

    expected_files: list[ExpectedFileSpec] = []
    for index, expected in enumerate(raw.get("expected_files", [])):
        file_context = f"{context}.expected_files[{index}]"
        if not isinstance(expected, dict):
            raise ValidationError(f"{file_context} must be a table")
        target = _required(expected, "path", str, file_context)
        safe_relative_path(target, label=f"{file_context}.path")
        content = expected.get("content")
        source = expected.get("source")
        if (content is None) == (source is None):
            raise ValidationError(f"{file_context} requires exactly one of content or source")
        if content is not None and not isinstance(content, str):
            raise ValidationError(f"{file_context}.content must be a string")
        if source is not None:
            if not isinstance(source, str):
                raise ValidationError(f"{file_context}.source must be a string")
            resolve_under(root, source)
        expected_files.append(ExpectedFileSpec(path=target, content=content, source=source))

    return TestCase(
        id=test_id,
        argv=argv,
        stdin=stdin,
        expected_stdout=expected_stdout,
        expected_stderr=expected_stderr,
        expected_exit=expected_exit,
        timeout_ms=timeout_ms,
        comparison=comparison,
        selected_characters=selected,
        fixtures=tuple(fixtures),
        expected_files=tuple(expected_files),
    )


def _parse_question(raw: Mapping[str, Any], *, root: Path, index: int) -> Question:
    context = f"questions[{index}]"
    question_id = _identifier(_required(raw, "id", str, context), context=f"{context}.id")
    title = _required(raw, "title", str, context)
    kind = _required(raw, "kind", str, context)
    if kind not in {"c_program", "c_function", "mips_program", "text"}:
        raise ValidationError(f"{context}.kind is unsupported: {kind!r}")
    points = _decimal(_required(raw, "points", (int, float), context), context=f"{context}.points")
    pass_points = _decimal(raw.get("pass_points", points), context=f"{context}.pass_points")
    if points <= 0 or pass_points > points:
        raise ValidationError(f"{context}: points must be positive and pass_points <= points")

    prompt_raw = raw.get("prompt")
    if prompt_raw is not None and not isinstance(prompt_raw, str):
        raise ValidationError(f"{context}.prompt must be a path string")
    if prompt_raw is not None:
        resolve_under(root, prompt_raw)
    difficulty = raw.get("difficulty", 3)
    if isinstance(difficulty, bool) or not isinstance(difficulty, int):
        raise ValidationError(f"{context}.difficulty must be an integer")
    if difficulty < 1 or difficulty > 5:
        raise ValidationError(f"{context}.difficulty must be between 1 and 5")
    track = raw.get("track", "normal")
    if track not in {"normal", "challenge"}:
        raise ValidationError(f"{context}.track must be 'normal' or 'challenge'")
    tags = _string_list(raw.get("tags", []), context=f"{context}.tags", nonempty=False)
    if len(tags) != len(set(tags)):
        raise ValidationError(f"{context}.tags must not contain duplicates")
    estimated_minutes_raw = raw.get("estimated_minutes")
    estimated_minutes = None
    if estimated_minutes_raw is not None:
        estimated_minutes = _bounded_integer(
            estimated_minutes_raw,
            context=f"{context}.estimated_minutes",
            maximum=180,
        )

    starter_files = _string_list(raw.get("starter_files", []), context=f"{context}.starter_files")
    submission_files = _string_list(
        raw.get("submission_files", []), context=f"{context}.submission_files"
    )
    for path in starter_files:
        resolve_under(root, path)
        Pack.starter_target(path)
    for path in submission_files:
        safe_relative_path(path, label=f"{context}.submission_files")

    build_raw = raw.get("build", {})
    if not isinstance(build_raw, dict):
        raise ValidationError(f"{context}.build must be a table")
    build_argv = _validate_argv(
        build_raw.get("argv", []), context=f"{context}.build.argv", allow_empty=True
    )
    if kind.startswith("c_") and not build_argv:
        raise ValidationError(f"{context}: C questions require build.argv")

    groups_raw = raw.get("test_groups", [])
    if not isinstance(groups_raw, list) or not groups_raw:
        raise ValidationError(f"{context}.test_groups must be a non-empty array of tables")
    groups: list[TestGroup] = []
    group_ids: set[str] = set()
    test_ids: set[str] = set()
    for group_index, group_raw in enumerate(groups_raw):
        group_context = f"{context}.test_groups[{group_index}]"
        if not isinstance(group_raw, dict):
            raise ValidationError(f"{group_context} must be a table")
        group_id = _identifier(
            _required(group_raw, "id", str, group_context), context=f"{group_context}.id"
        )
        if group_id in group_ids:
            raise ValidationError(f"{context}: duplicate test group {group_id!r}")
        group_ids.add(group_id)
        try:
            visibility = TestVisibility(group_raw.get("visibility", "public"))
        except ValueError as exc:
            raise ValidationError(f"{group_context}.visibility is invalid") from exc
        group_points = _decimal(
            _required(group_raw, "points", (int, float), group_context),
            context=f"{group_context}.points",
        )
        tests_raw = group_raw.get("tests", [])
        if not isinstance(tests_raw, list) or not tests_raw:
            raise ValidationError(f"{group_context}.tests must be a non-empty array")
        tests: list[TestCase] = []
        for test_index, test_raw in enumerate(tests_raw):
            if not isinstance(test_raw, dict):
                raise ValidationError(f"{group_context}.tests[{test_index}] must be a table")
            test = _parse_test(
                test_raw,
                root=root,
                context=f"{group_context}.tests[{test_index}]",
            )
            qualified_id = f"{group_id}/{test.id}"
            if qualified_id in test_ids:
                raise ValidationError(f"{context}: duplicate test {qualified_id!r}")
            test_ids.add(qualified_id)
            tests.append(test)
        groups.append(
            TestGroup(id=group_id, visibility=visibility, points=group_points, tests=tuple(tests))
        )

    automatic_points = sum((group.points for group in groups), Decimal(0))
    if automatic_points > points:
        raise ValidationError(f"{context}: automatic test-group points exceed question points")
    if pass_points > automatic_points:
        raise ValidationError(f"{context}: pass_points exceed automatically assessable points")

    return Question(
        id=question_id,
        title=title,
        kind=kind,
        points=points,
        pass_points=pass_points,
        starter_files=starter_files,
        submission_files=submission_files,
        build_argv=build_argv,
        test_groups=tuple(groups),
        prompt=prompt_raw,
        difficulty=difficulty,
        track=track,
        tags=tags,
        estimated_minutes=estimated_minutes,
    )


def _pack_files(root: Path) -> Iterable[tuple[Path, PurePosixPath]]:
    resolved_root = root.resolve()
    for path in sorted(root.rglob("*")):
        relative = PurePosixPath(path.relative_to(root).as_posix())
        if relative.parts[0] in _EXCLUDED_PACK_DIRECTORIES:
            continue
        if path.is_symlink():
            try:
                link_target = Path(os.readlink(path))
                unresolved = (
                    link_target if link_target.is_absolute() else path.parent / link_target
                )
                resolved = unresolved.resolve(strict=True)
            except (OSError, RuntimeError) as exc:
                raise ValidationError(f"pack contains a broken symlink: {relative}") from exc
            if not resolved.is_relative_to(resolved_root):
                raise ValidationError(f"pack symlink escapes its root: {relative}")
            if not resolved.is_file():
                raise ValidationError(f"pack symlink must target a regular file: {relative}")
            yield resolved, relative
        elif path.is_file():
            resolved = path.resolve(strict=True)
            if not resolved.is_relative_to(resolved_root):
                raise ValidationError(f"pack file escapes its root: {relative}")
            yield resolved, relative


def copy_pack_files(root: Path, destination: Path) -> None:
    if destination.exists():
        if any(destination.iterdir()):
            raise ValidationError(f"pack snapshot destination is not empty: {destination}")
    else:
        destination.mkdir(parents=True)
    for source, relative in _pack_files(root):
        target = destination.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def pack_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path, relative in _pack_files(root):
        digest.update(relative.as_posix().encode())
        digest.update(b"\x00")
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\x00")
    return digest.hexdigest()


def snapshot_pack(pack: Pack, destination: Path) -> Pack:
    """Atomically create or verify the author-file-free pack used by one attempt."""
    if destination.exists():
        frozen = load_pack(destination)
        if frozen.digest != pack.digest:
            raise ValidationError("existing attempt pack snapshot has the wrong digest")
        return frozen

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        copy_pack_files(pack.root, temporary)
        frozen = load_pack(temporary)
        if frozen.digest != pack.digest:
            raise ValidationError("attempt pack snapshot digest does not match its source")
        for path in temporary.rglob("*"):
            if path.is_file():
                path.chmod(path.stat().st_mode & ~0o222)
        os.replace(temporary, destination)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

    frozen = load_pack(destination)
    if frozen.digest != pack.digest:
        raise ValidationError("published attempt pack snapshot failed verification")
    return frozen


def _author_files(pack: Pack) -> Iterable[tuple[Path, PurePosixPath]]:
    source_root = pack.root / "solutions"
    if not source_root.is_dir():
        return
    resolved_pack = pack.root.resolve()
    for source in sorted(source_root.rglob("*")):
        if source.is_symlink():
            raise ValidationError(
                f"author material must not be a symlink: {source.relative_to(pack.root)}"
            )
        if not source.is_file():
            continue
        resolved = source.resolve(strict=True)
        if not resolved.is_relative_to(resolved_pack):
            raise ValidationError(
                f"author material escapes the pack: {source.relative_to(pack.root)}"
            )
        yield resolved, PurePosixPath(source.relative_to(pack.root).as_posix())


def snapshot_author_materials(pack: Pack, destination: Path) -> str:
    """Freeze solution material beside, but never inside, the student pack snapshot."""
    files = list(_author_files(pack))
    digest = hashlib.sha256()
    entries: list[dict[str, object]] = []
    for source, relative in files:
        content = source.read_bytes()
        file_digest = hashlib.sha256(content).hexdigest()
        digest.update(relative.as_posix().encode())
        digest.update(b"\x00")
        digest.update(content)
        digest.update(b"\x00")
        entries.append({"path": relative.as_posix(), "sha256": file_digest, "size": len(content)})
    author_digest = digest.hexdigest()
    if destination.exists():
        manifest = destination / "manifest.json"
        try:
            recorded = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValidationError("existing author-material snapshot is invalid") from exc
        if recorded.get("digest") != author_digest:
            raise ValidationError("existing author-material snapshot has the wrong digest")
        return author_digest

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        for source, relative in files:
            target = temporary.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        (temporary / "manifest.json").write_text(
            json.dumps(
                {"schema_version": 1, "digest": author_digest, "files": entries},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        for path in temporary.rglob("*"):
            if path.is_file():
                path.chmod(path.stat().st_mode & ~0o222)
        os.replace(temporary, destination)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    return author_digest


def load_pack(path: Path | str) -> Pack:
    root = Path(path).expanduser().resolve()
    manifest = root / "pack.toml"
    if not manifest.is_file():
        raise ValidationError(f"pack manifest not found: {manifest}")
    try:
        raw = tomllib.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ValidationError(f"cannot read pack manifest: {exc}") from exc

    schema_version = _required(raw, "schema_version", int, "pack")
    if schema_version != 1:
        raise ValidationError(f"unsupported pack schema version: {schema_version}")
    pack_id = _identifier(_required(raw, "id", str, "pack"), context="pack.id")
    version = _required(raw, "version", str, "pack")
    if not _VERSION_PATTERN.fullmatch(version):
        raise ValidationError("pack.version must be semantic versioning form X.Y.Z")
    title = _required(raw, "title", str, "pack")
    course = _required(raw, "course", str, "pack")
    profile = _identifier(_required(raw, "profile", str, "pack"), context="pack.profile")
    if profile not in {"comp1511", "comp1521"}:
        raise ValidationError(f"unsupported course profile: {profile}")
    author = _required(raw, "author", str, "pack")
    license_name = _required(raw, "license", str, "pack")
    if not license_name.strip():
        raise ValidationError("pack.license may not be blank")
    paper = _required(raw, "paper", str, "pack")
    resolve_under(root, paper)
    reading_time = _required(raw, "reading_time_seconds", int, "pack")
    working_time = _required(raw, "working_time_seconds", int, "pack")
    if reading_time < 0 or working_time <= 0:
        raise ValidationError("reading time must be non-negative and working time positive")

    environment_raw = _required(raw, "environment", dict, "pack")
    cpus_raw = environment_raw.get("cpus", 2.0)
    if isinstance(cpus_raw, bool) or not isinstance(cpus_raw, (int, float)):
        raise ValidationError("environment.cpus must be a number")
    cpus = float(cpus_raw)
    if not math.isfinite(cpus) or cpus <= 0 or cpus > _MAX_CPUS:
        raise ValidationError(f"environment.cpus must be greater than 0 and at most {_MAX_CPUS:g}")
    environment = EnvironmentSpec(
        image=_required(environment_raw, "image", str, "environment"),
        network=_required(environment_raw, "network", str, "environment"),
        cpus=cpus,
        memory_mb=_bounded_integer(
            environment_raw.get("memory_mb", 1024),
            context="environment.memory_mb",
            maximum=_MAX_MEMORY_MB,
        ),
        pids=_bounded_integer(
            environment_raw.get("pids", 128),
            context="environment.pids",
            maximum=_MAX_PIDS,
        ),
        output_limit_kb=_bounded_integer(
            environment_raw.get("output_limit_kb", 256),
            context="environment.output_limit_kb",
            maximum=_MAX_OUTPUT_LIMIT_KB,
        ),
    )
    if environment.network != "none":
        raise ValidationError("schema v1 packs must declare environment.network = 'none'")
    expected_image = f"csetty/{profile}:dev"
    if environment.image != expected_image:
        raise ValidationError(
            f"environment.image must be {expected_image!r} for profile {profile!r}"
        )
    resources: list[ResourceSpec] = []
    for index, resource_raw in enumerate(raw.get("resources", [])):
        context = f"resources[{index}]"
        if not isinstance(resource_raw, dict):
            raise ValidationError(f"{context} must be a table")
        resource_path = _required(resource_raw, "path", str, context)
        resolve_under(root, resource_path)
        resources.append(
            ResourceSpec(path=resource_path, label=_required(resource_raw, "label", str, context))
        )

    questions_raw = raw.get("questions", [])
    if not isinstance(questions_raw, list) or not questions_raw:
        raise ValidationError("pack.questions must be a non-empty array")
    questions: list[Question] = []
    question_ids: set[str] = set()
    submission_paths: set[str] = set()
    for index, question_raw in enumerate(questions_raw):
        if not isinstance(question_raw, dict):
            raise ValidationError(f"questions[{index}] must be a table")
        question = _parse_question(question_raw, root=root, index=index)
        if question.id in question_ids:
            raise ValidationError(f"duplicate question id: {question.id}")
        question_ids.add(question.id)
        for submission_path in question.submission_files:
            if submission_path in submission_paths:
                raise ValidationError(f"submission path is shared by questions: {submission_path}")
            submission_paths.add(submission_path)
        questions.append(question)

    hurdles: list[Hurdle] = []
    hurdle_ids: set[str] = set()
    for index, hurdle_raw in enumerate(raw.get("hurdles", [])):
        context = f"hurdles[{index}]"
        if not isinstance(hurdle_raw, dict):
            raise ValidationError(f"{context} must be a table")
        hurdle_id = _identifier(_required(hurdle_raw, "id", str, context), context=f"{context}.id")
        if hurdle_id in hurdle_ids:
            raise ValidationError(f"duplicate hurdle id: {hurdle_id}")
        hurdle_ids.add(hurdle_id)
        hurdle_questions = _string_list(
            _required(hurdle_raw, "question_ids", list, context), context=f"{context}.question_ids"
        )
        unknown = set(hurdle_questions) - question_ids
        if unknown:
            raise ValidationError(f"{context} references unknown questions: {sorted(unknown)}")
        minimum = _required(hurdle_raw, "min_passed_questions", int, context)
        if minimum <= 0 or minimum > len(hurdle_questions):
            raise ValidationError(f"{context}.min_passed_questions is outside the valid range")
        hurdles.append(
            Hurdle(
                id=hurdle_id,
                label=_required(hurdle_raw, "label", str, context),
                question_ids=hurdle_questions,
                min_passed_questions=minimum,
            )
        )

    warnings: list[str] = []
    for question in questions:
        if not any(group.visibility is TestVisibility.PUBLIC for group in question.test_groups):
            warnings.append(f"{question.id} has no public tests")
        if question.automatic_points < question.points:
            manual_points = question.points - question.automatic_points
            warnings.append(f"{question.id} has {manual_points} points not automatically assessed")

    return Pack(
        root=root,
        schema_version=schema_version,
        id=pack_id,
        version=version,
        title=title,
        course=course,
        profile=profile,
        author=author,
        license=license_name,
        paper=paper,
        reading_time_seconds=reading_time,
        working_time_seconds=working_time,
        environment=environment,
        resources=tuple(resources),
        questions=tuple(questions),
        hurdles=tuple(hurdles),
        digest=pack_digest(root),
        warnings=tuple(warnings),
    )


class PackRepository:
    def __init__(self, roots: Iterable[Path] | None = None) -> None:
        if roots is None:
            configured = os.environ.get("CSETTY_PACKS_DIR")
            candidates: list[Path] = []
            if configured:
                candidates.extend(Path(item) for item in configured.split(os.pathsep) if item)
            candidates.append(Path.cwd() / "packs")
            candidates.append(assets_root() / "packs")
            roots = candidates
        self.roots = tuple(Path(root).expanduser().resolve() for root in roots)

    def paths(self) -> tuple[Path, ...]:
        found: list[Path] = []
        seen: set[Path] = set()
        for root in self.roots:
            if not root.is_dir():
                continue
            if (root / "pack.toml").is_file() and root not in seen:
                found.append(root)
                seen.add(root)
            for manifest in sorted(root.glob("*/pack.toml")):
                directory = manifest.parent.resolve()
                if directory not in seen:
                    found.append(directory)
                    seen.add(directory)
        return tuple(found)

    def list(self) -> tuple[Pack, ...]:
        unique: dict[tuple[str, str], Pack] = {}
        for pack in (load_pack(path) for path in self.paths()):
            identity = (pack.id, pack.version)
            existing = unique.get(identity)
            if existing is not None and existing.digest != pack.digest:
                raise ValidationError(
                    f"conflicting installed pack identity: {pack.id}@{pack.version}"
                )
            unique.setdefault(identity, pack)
        return tuple(sorted(unique.values(), key=lambda item: (item.course, item.id, item.version)))

    def get(self, selector: str) -> Pack:
        selector_id, separator, selector_version = selector.partition("@")
        matches = [
            pack
            for pack in self.list()
            if pack.id == selector_id and (not separator or pack.version == selector_version)
        ]
        if not matches:
            candidate = Path(selector)
            if candidate.exists():
                return load_pack(candidate)
            raise ValidationError(f"exam pack not found: {selector}")
        if len(matches) > 1:
            versions = ", ".join(pack.version for pack in matches)
            raise ValidationError(
                f"pack {selector_id!r} has multiple versions ({versions}); use id@version"
            )
        return matches[0]
