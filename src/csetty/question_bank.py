from __future__ import annotations

import json
import random
import shutil
import tomllib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from decimal import Decimal
from pathlib import Path
from typing import Any

from .assets import assets_root
from .errors import ValidationError
from .pack import Pack, Question, _identifier, _parse_question, load_pack
from .util import resolve_under, safe_relative_path

_PROMPT_HEADINGS = (
    "## Background",
    "## Requirements",
    "## Examples",
    "## Implementation notes",
)
_SOLUTION_HEADINGS = ("## Approach", "## Correctness", "## Complexity", "## Common pitfalls")


@dataclass(frozen=True)
class BankQuestion:
    root: Path
    question: Question
    slots: tuple[str, ...]
    weeks: tuple[int, ...]
    solution: str

    def solution_text(self) -> str:
        return resolve_under(self.root, self.solution).read_text(encoding="utf-8")

    def reference_file(self, relative: str) -> Path:
        safe = safe_relative_path(relative, label="reference solution path")
        return resolve_under(self.root, Path("reference").joinpath(*safe.parts).as_posix())


@dataclass(frozen=True)
class QuestionBank:
    root: Path
    schema_version: int
    id: str
    title: str
    course: str
    profile: str
    author: str
    license: str
    allowed_tags: tuple[str, ...]
    allowed_slots: tuple[str, ...]
    questions: tuple[BankQuestion, ...]

    def stats(self) -> dict[str, Any]:
        by_track: dict[str, int] = {}
        by_difficulty: dict[str, int] = {}
        by_tag: dict[str, int] = {}
        by_slot: dict[str, int] = {}
        for item in self.questions:
            question = item.question
            by_track[question.track] = by_track.get(question.track, 0) + 1
            difficulty = str(question.difficulty)
            by_difficulty[difficulty] = by_difficulty.get(difficulty, 0) + 1
            for tag in question.tags:
                by_tag[tag] = by_tag.get(tag, 0) + 1
            for slot in item.slots:
                by_slot[slot] = by_slot.get(slot, 0) + 1
        return {
            "id": self.id,
            "course": self.course,
            "total": len(self.questions),
            "by_track": dict(sorted(by_track.items())),
            "by_difficulty": dict(sorted(by_difficulty.items())),
            "by_tag": dict(sorted(by_tag.items())),
            "by_slot": dict(sorted(by_slot.items())),
        }


@dataclass(frozen=True)
class BlueprintSlot:
    id: str
    bank_slot: str
    points: Decimal
    require_track: str | None = None
    require_any_tags: tuple[str, ...] = ()


_BLUEPRINTS: dict[str, tuple[BlueprintSlot, ...]] = {
    "comp1511": (
        BlueprintSlot("q1", "list_hurdle", Decimal(12)),
        BlueprintSlot("q2", "array_hurdle", Decimal(12)),
        BlueprintSlot("q3", "list_hurdle", Decimal(12)),
        BlueprintSlot("q4", "array_hurdle", Decimal(12)),
        BlueprintSlot("q5", "short", Decimal(5)),
        BlueprintSlot("q6", "short", Decimal(5)),
        BlueprintSlot("q7", "short", Decimal(5)),
        BlueprintSlot("q8", "short", Decimal(5)),
        BlueprintSlot("q9", "medium", Decimal(11)),
        BlueprintSlot("q10", "medium", Decimal(11)),
        BlueprintSlot("q11", "whole_program", Decimal(10)),
    ),
    "comp1521": (
        BlueprintSlot("q1", "foundation", Decimal(10), require_any_tags=("file-io",)),
        BlueprintSlot(
            "q2",
            "foundation",
            Decimal(10),
            require_any_tags=("bitwise", "integer-representation"),
        ),
        BlueprintSlot(
            "q3",
            "foundation",
            Decimal(10),
            require_any_tags=("mips-basics", "mips-control", "mips-data", "mips-functions"),
        ),
        BlueprintSlot("q4", "foundation", Decimal(10)),
        BlueprintSlot("q5", "unicode", Decimal(10)),
        BlueprintSlot("q6", "advanced_systems", Decimal(10)),
        BlueprintSlot("q7", "advanced_systems", Decimal(10)),
        BlueprintSlot("q8", "advanced_systems", Decimal(10)),
        BlueprintSlot("q9", "processes_threads", Decimal(10)),
        BlueprintSlot("q10", "challenge_combo", Decimal(10), require_track="challenge"),
    ),
}


def _required(
    mapping: Mapping[str, Any], key: str, expected: type[Any], *, context: str
) -> Any:
    if key not in mapping:
        raise ValidationError(f"{context}: missing required field {key!r}")
    value = mapping[key]
    if not isinstance(value, expected):
        raise ValidationError(f"{context}.{key} must be {expected.__name__}")
    return value


def _string_tuple(value: object, *, context: str, nonempty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, list) or (nonempty and not value):
        raise ValidationError(f"{context} must be a {'non-empty ' if nonempty else ''}list")
    if not all(isinstance(item, str) and item for item in value):
        raise ValidationError(f"{context} entries must be non-empty strings")
    return tuple(value)


def _read_structured_markdown(path: Path, headings: Sequence[str], *, context: str) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"cannot read {context}: {exc}") from exc
    if len(text.strip()) < 120:
        raise ValidationError(f"{context} is too short to be a detailed teaching document")
    missing = [heading for heading in headings if heading.casefold() not in text.casefold()]
    if missing:
        raise ValidationError(f"{context} is missing headings: {', '.join(missing)}")
    return text


def _load_bank_question(
    path: Path, *, index: int, allowed_tags: set[str], allowed_slots: set[str]
) -> BankQuestion:
    context = f"questions[{index}]"
    try:
        raw_value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read {path}: {exc}") from exc
    if not isinstance(raw_value, dict):
        raise ValidationError(f"{path} must contain a JSON object")
    raw: dict[str, Any] = {str(key): value for key, value in raw_value.items()}
    if raw.get("schema_version") != 1:
        raise ValidationError(f"{context}.schema_version must be 1")
    _required(raw, "prompt", str, context=context)
    slots = _string_tuple(raw.get("slots"), context=f"{context}.slots")
    unknown_slots = set(slots) - allowed_slots
    if unknown_slots:
        raise ValidationError(f"{context}.slots contains unknown values: {sorted(unknown_slots)}")
    if len(slots) != len(set(slots)):
        raise ValidationError(f"{context}.slots must not contain duplicates")
    weeks_value = raw.get("weeks", [])
    if not isinstance(weeks_value, list) or not all(
        isinstance(week, int) and not isinstance(week, bool) and 1 <= week <= 10
        for week in weeks_value
    ):
        raise ValidationError(f"{context}.weeks must contain integers from 1 to 10")
    weeks = tuple(weeks_value)
    if len(weeks) != len(set(weeks)):
        raise ValidationError(f"{context}.weeks must not contain duplicates")
    solution = _required(raw, "solution", str, context=context)
    question = _parse_question(raw, root=path.parent, index=index)
    if question.id != path.parent.name:
        raise ValidationError(
            f"{context}.id must match its directory name {path.parent.name!r}"
        )
    if not question.tags:
        raise ValidationError(f"{context}.tags must contain at least one topic tag")
    unknown_tags = set(question.tags) - allowed_tags
    if unknown_tags:
        raise ValidationError(f"{context}.tags contains unknown values: {sorted(unknown_tags)}")
    assert question.prompt is not None
    _read_structured_markdown(
        resolve_under(path.parent, question.prompt),
        _PROMPT_HEADINGS,
        context=f"{context}.prompt",
    )
    _read_structured_markdown(
        resolve_under(path.parent, solution),
        _SOLUTION_HEADINGS,
        context=f"{context}.solution",
    )
    starter_targets = {
        Pack.starter_target(starter).as_posix() for starter in question.starter_files
    }
    missing_starters = set(question.submission_files) - starter_targets
    if missing_starters:
        raise ValidationError(
            f"{context} has no starter file for submissions: {sorted(missing_starters)}"
        )
    item = BankQuestion(
        root=path.parent,
        question=question,
        slots=slots,
        weeks=weeks,
        solution=solution,
    )
    for relative in question.submission_files:
        reference = item.reference_file(relative)
        if not reference.is_file() or reference.is_symlink():
            raise ValidationError(f"{context} reference solution is missing {relative}")
    return item


def load_question_bank(path: Path | str) -> QuestionBank:
    requested = Path(path).expanduser()
    if str(path) in _BLUEPRINTS and not requested.exists():
        requested = assets_root() / "question_bank" / str(path)
    root = requested.resolve()
    manifest = root / "bank.toml"
    if not manifest.is_file():
        raise ValidationError(f"question-bank manifest not found: {manifest}")
    try:
        raw = tomllib.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ValidationError(f"cannot read question-bank manifest: {exc}") from exc
    if raw.get("schema_version") != 1:
        raise ValidationError("question-bank schema_version must be 1")
    profile = _identifier(_required(raw, "profile", str, context="bank"), context="bank.profile")
    if profile not in _BLUEPRINTS:
        raise ValidationError(f"unsupported question-bank profile: {profile}")
    allowed_tags = _string_tuple(raw.get("allowed_tags"), context="bank.allowed_tags")
    allowed_slots = _string_tuple(raw.get("allowed_slots"), context="bank.allowed_slots")
    if len(allowed_tags) != len(set(allowed_tags)):
        raise ValidationError("bank.allowed_tags must not contain duplicates")
    if len(allowed_slots) != len(set(allowed_slots)):
        raise ValidationError("bank.allowed_slots must not contain duplicates")
    required_slots = {slot.bank_slot for slot in _BLUEPRINTS[profile]}
    if not required_slots.issubset(allowed_slots):
        missing_slots = sorted(required_slots - set(allowed_slots))
        raise ValidationError(
            f"bank.allowed_slots is missing blueprint slots: {missing_slots}"
        )
    question_paths = sorted((root / "questions").glob("*/question.json"))
    if not question_paths:
        raise ValidationError("question bank contains no questions")
    questions = tuple(
        _load_bank_question(
            question_path,
            index=index,
            allowed_tags=set(allowed_tags),
            allowed_slots=set(allowed_slots),
        )
        for index, question_path in enumerate(question_paths)
    )
    ids = [item.question.id for item in questions]
    if len(ids) != len(set(ids)):
        raise ValidationError("question bank contains duplicate question IDs")
    course = _required(raw, "course", str, context="bank")
    expected_course = profile.upper()
    if course != expected_course:
        raise ValidationError(f"bank.course must be {expected_course!r} for {profile}")
    return QuestionBank(
        root=root,
        schema_version=1,
        id=_identifier(_required(raw, "id", str, context="bank"), context="bank.id"),
        title=_required(raw, "title", str, context="bank"),
        course=course,
        profile=profile,
        author=_required(raw, "author", str, context="bank"),
        license=_required(raw, "license", str, context="bank"),
        allowed_tags=allowed_tags,
        allowed_slots=allowed_slots,
        questions=questions,
    )


def select_exam(bank: QuestionBank, *, seed: int) -> tuple[tuple[BlueprintSlot, BankQuestion], ...]:
    generator = random.Random(seed)
    selected_ids: set[str] = set()
    selected: list[tuple[BlueprintSlot, BankQuestion]] = []
    for slot in _BLUEPRINTS[bank.profile]:
        candidates = [
            item
            for item in bank.questions
            if slot.bank_slot in item.slots
            and item.question.points == slot.points
            and item.question.id not in selected_ids
            and (slot.require_track is None or item.question.track == slot.require_track)
            and (
                not slot.require_any_tags
                or bool(set(slot.require_any_tags).intersection(item.question.tags))
            )
        ]
        if not candidates:
            raise ValidationError(
                f"question bank cannot fill {slot.id}: slot={slot.bank_slot}, "
                f"points={slot.points}, tags={list(slot.require_any_tags)}"
            )
        chosen = generator.choice(sorted(candidates, key=lambda item: item.question.id))
        selected_ids.add(chosen.question.id)
        selected.append((slot, chosen))
    return tuple(selected)


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _toml_array(values: Iterable[str]) -> str:
    return "[" + ", ".join(_toml_string(value) for value in values) + "]"


def _decimal_text(value: Decimal) -> str:
    return format(value, "f")


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _emit_question(
    *, slot: BlueprintSlot, item: BankQuestion, output: Path
) -> tuple[list[str], Question]:
    source = item.question
    prompt_path = f"questions/{slot.id}.md"
    _copy_file(resolve_under(item.root, source.prompt or ""), output / prompt_path)
    starter_files: list[str] = []
    for relative in source.starter_files:
        target = Pack.starter_target(relative).as_posix()
        destination = f"starter/{target}"
        _copy_file(resolve_under(item.root, relative), output / destination)
        starter_files.append(destination)
    for relative in source.submission_files:
        _copy_file(item.reference_file(relative), output / "solutions" / "reference" / relative)
    _copy_file(
        resolve_under(item.root, item.solution),
        output / "solutions" / "explanations" / f"{slot.id}.md",
    )

    lines = [
        "[[questions]]",
        f"id = {_toml_string(slot.id)}",
        f"title = {_toml_string(source.title)}",
        f"kind = {_toml_string(source.kind)}",
        f"points = {_decimal_text(source.points)}",
        f"pass_points = {_decimal_text(source.pass_points)}",
        f"prompt = {_toml_string(prompt_path)}",
        f"difficulty = {source.difficulty}",
        f"track = {_toml_string(source.track)}",
        f"tags = {_toml_array(source.tags)}",
    ]
    if source.estimated_minutes is not None:
        lines.append(f"estimated_minutes = {source.estimated_minutes}")
    lines.extend(
        (
            f"starter_files = {_toml_array(starter_files)}",
            f"submission_files = {_toml_array(source.submission_files)}",
            "[questions.build]",
            f"argv = {_toml_array(source.build_argv)}",
        )
    )
    for group in source.test_groups:
        lines.extend(
            (
                "[[questions.test_groups]]",
                f"id = {_toml_string(group.id)}",
                f"visibility = {_toml_string(group.visibility.value)}",
                f"points = {_decimal_text(group.points)}",
            )
        )
        for test in group.tests:
            lines.extend(
                (
                    "[[questions.test_groups.tests]]",
                    f"id = {_toml_string(test.id)}",
                    f"argv = {_toml_array(test.argv)}",
                    f"stdin = {_toml_string(test.stdin)}",
                    f"timeout_ms = {test.timeout_ms}",
                    f"comparison = {_toml_string(test.comparison)}",
                )
            )
            if test.selected_characters is not None:
                lines.append(f"selected_characters = {_toml_string(test.selected_characters)}")
            if test.expected_stdout is not None:
                lines.append(f"expected_stdout = {_toml_string(test.expected_stdout)}")
            if test.expected_stderr is not None:
                lines.append(f"expected_stderr = {_toml_string(test.expected_stderr)}")
            if test.expected_exit is not None:
                lines.append(f"expected_exit = {test.expected_exit}")
            for fixture_index, fixture in enumerate(test.fixtures):
                fixture_name = Path(fixture.source).name
                fixture_path = f"tests/{slot.id}/{test.id}-{fixture_index}-{fixture_name}"
                _copy_file(resolve_under(item.root, fixture.source), output / fixture_path)
                lines.extend(
                    (
                        "[[questions.test_groups.tests.fixtures]]",
                        f"source = {_toml_string(fixture_path)}",
                        f"path = {_toml_string(fixture.path)}",
                    )
                )
            for expected in test.expected_files:
                lines.extend(
                    (
                        "[[questions.test_groups.tests.expected_files]]",
                        f"path = {_toml_string(expected.path)}",
                    )
                )
                content = expected.content
                if content is None:
                    assert expected.source is not None
                    content = resolve_under(item.root, expected.source).read_text(encoding="utf-8")
                lines.append(f"content = {_toml_string(content)}")
    emitted = replace(
        source,
        id=slot.id,
        prompt=prompt_path,
        starter_files=tuple(starter_files),
    )
    return lines, emitted


def build_exam_pack(
    bank: QuestionBank, *, destination: Path, seed: int, version: str = "1.0.0"
) -> Pack:
    destination = destination.expanduser().resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValidationError(f"exam-pack destination is not empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    selection = select_exam(bank, seed=seed)
    question_lines: list[str] = []
    emitted_questions: list[Question] = []
    for slot, item in selection:
        lines, emitted = _emit_question(slot=slot, item=item, output=destination)
        question_lines.extend(lines)
        emitted_questions.append(emitted)

    paper_lines = [
        f"# {bank.course} original generated practice exam",
        "",
        "This local simulation paper is original material and is not made or managed by UNSW.",
        "",
        "## Questions",
        "",
    ]
    for slot, item in selection:
        paper_lines.append(
            f"- **{slot.id.upper()} — {item.question.title}** "
            f"({item.question.points} marks, difficulty {item.question.difficulty}/5, "
            f"{item.question.track})"
        )
    paper = destination / "paper" / "index.md"
    paper.parent.mkdir(parents=True, exist_ok=True)
    paper.write_text("\n".join(paper_lines) + "\n", encoding="utf-8")

    pack_id = f"{bank.profile}-generated-{seed}"
    header = [
        "schema_version = 1",
        f"id = {_toml_string(pack_id)}",
        f"version = {_toml_string(version)}",
        f"title = {_toml_string(f'{bank.course} Original Generated Practice Exam')}",
        f"course = {_toml_string(bank.course)}",
        f"profile = {_toml_string(bank.profile)}",
        f"author = {_toml_string(bank.author)}",
        f"license = {_toml_string(bank.license)}",
        'paper = "paper/index.md"',
        "reading_time_seconds = 600",
        "working_time_seconds = 10800",
        "",
        "[environment]",
        f"image = {_toml_string(f'csetty/{bank.profile}:dev')}",
        'network = "none"',
        "cpus = 2",
        "memory_mb = 1024",
        "pids = 128",
        "output_limit_kb = 256",
        "",
    ]
    if bank.profile == "comp1511":
        question_lines.extend(
            (
                "[[hurdles]]",
                'id = "linked_list_hurdle"',
                'label = "Linked-list hurdle"',
                'question_ids = ["q1", "q3"]',
                "min_passed_questions = 1",
                "[[hurdles]]",
                'id = "array_hurdle"',
                'label = "Array hurdle"',
                'question_ids = ["q2", "q4"]',
                "min_passed_questions = 1",
            )
        )
    (destination / "pack.toml").write_text(
        "\n".join((*header, *question_lines)) + "\n", encoding="utf-8"
    )
    pack = load_pack(destination)
    expected_total = sum((item.points for item in emitted_questions), Decimal(0))
    if expected_total != Decimal(100) or pack.total_points != Decimal(100):
        raise ValidationError("generated exam blueprint must total exactly 100 points")
    return pack


def build_verification_pack(
    bank: QuestionBank, *, destination: Path, version: str = "1.0.0"
) -> Pack:
    """Build an author-only pack containing every question in a bank.

    The resulting pack exists solely so the ordinary isolated judge can run
    every reference solution and declared test. It is not a student paper and
    therefore is not constrained to the 100-point course blueprint.
    """

    destination = destination.expanduser().resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValidationError(f"verification-pack destination is not empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)

    question_lines: list[str] = []
    for item in bank.questions:
        slot = BlueprintSlot(
            id=item.question.id,
            bank_slot=item.slots[0],
            points=item.question.points,
        )
        lines, _emitted = _emit_question(slot=slot, item=item, output=destination)
        question_lines.extend(lines)

    paper_lines = [
        f"# {bank.course} full question-bank verification pack",
        "",
        "Author-only local verification material; this is not a student exam paper.",
        "",
        "## Questions",
        "",
    ]
    paper_lines.extend(
        f"- **{item.question.id} — {item.question.title}**"
        for item in bank.questions
    )
    paper = destination / "paper" / "index.md"
    paper.parent.mkdir(parents=True, exist_ok=True)
    paper.write_text("\n".join(paper_lines) + "\n", encoding="utf-8")

    pack_id = f"{bank.profile}-bank-verification"
    header = [
        "schema_version = 1",
        f"id = {_toml_string(pack_id)}",
        f"version = {_toml_string(version)}",
        f"title = {_toml_string(f'{bank.course} Full Question-Bank Verification')}",
        f"course = {_toml_string(bank.course)}",
        f"profile = {_toml_string(bank.profile)}",
        f"author = {_toml_string(bank.author)}",
        f"license = {_toml_string(bank.license)}",
        'paper = "paper/index.md"',
        "reading_time_seconds = 0",
        "working_time_seconds = 10800",
        "",
        "[environment]",
        f"image = {_toml_string(f'csetty/{bank.profile}:dev')}",
        'network = "none"',
        "cpus = 2",
        "memory_mb = 1024",
        "pids = 128",
        "output_limit_kb = 256",
        "",
    ]
    (destination / "pack.toml").write_text(
        "\n".join((*header, *question_lines)) + "\n", encoding="utf-8"
    )
    pack = load_pack(destination)
    if len(pack.questions) != len(bank.questions):
        raise ValidationError("verification pack did not preserve every bank question")
    return pack
