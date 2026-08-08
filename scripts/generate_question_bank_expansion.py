#!/usr/bin/env python3
# ruff: noqa: E501
"""Generate the second, scenario-rich half of the bundled question banks.

The generated artifacts are committed so installations never need this script
at runtime.  Keeping the source catalogue here makes the 150-question expansion
reviewable and reproducible instead of relying on opaque copied directories.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BANK_ROOT = ROOT / "question_bank"


@dataclass(frozen=True)
class Case:
    id: str
    stdin: str = ""
    args: tuple[str, ...] = ()
    fixtures: tuple[tuple[str, str, bytes], ...] = ()


@dataclass(frozen=True)
class AuthoredQuestion:
    id: str
    title: str
    course: str
    kind: str
    difficulty: int
    track: str
    tags: tuple[str, ...]
    weeks: tuple[int, ...]
    slot: str
    minutes: int
    background: str
    requirements: str
    implementation_notes: str
    idea: str
    steps: tuple[str, ...]
    correctness: str
    complexity: str
    pitfalls: str
    starter: str
    reference: str
    cases: tuple[Case, ...]
    oracle: Callable[[Case], tuple[str, str, int]]
    extension: str = ".c"
    build_flags: tuple[str, ...] = ()
    definition: str = ""


def _slug_source(question_id: str, extension: str) -> str:
    return f"{question_id.replace('-', '_')}{extension}"


def _points(slot: str) -> tuple[int, int]:
    if slot in {"list_hurdle", "array_hurdle"}:
        return 12, 6
    if slot == "short":
        return 5, 2
    if slot == "medium":
        return 11, 5
    if slot == "whole_program":
        return 10, 5
    return 10, 4


def _example_text(case: Case, stdout: str) -> str:
    sections: list[str] = []
    if case.args:
        sections.append(f"Command-line arguments: `{' '.join(case.args)}`")
    if case.fixtures:
        descriptions: list[str] = []
        for _source, target, content in case.fixtures:
            if not content:
                descriptions.append(f"- `{target}` is empty.")
                continue
            try:
                decoded = content.decode("utf-8")
            except UnicodeDecodeError:
                decoded = ""
            if decoded and all(character.isprintable() or character in "\n\r\t" for character in decoded):
                descriptions.append(
                    f"- `{target}` contains:\n\n  ```text\n"
                    + "\n".join(f"  {line}" for line in decoded.rstrip("\n").split("\n"))
                    + "\n  ```"
                )
            else:
                descriptions.append(f"- `{target}` contains the bytes `{content.hex()}` (hexadecimal).")
        sections.append("Files provided for this example:\n\n" + "\n".join(descriptions))
    if case.stdin:
        sections.append(f"Input:\n\n```text\n{case.stdin.rstrip(chr(10))}\n```")
    output = stdout.rstrip("\n")
    rendered_output = output if output else "(no output)"
    sections.append(f"Output:\n\n```text\n{rendered_output}\n```")
    return "\n\n".join(sections)


def _starter_instructions(question: AuthoredQuestion) -> str:
    prefix = question.id.rsplit("-", 1)[0]
    instructions = {
        "c1511-array": "Complete `static long long solve(const int *a, int n)`. The supplied `main` already reads the array and prints the returned value; do not replace the input/output code.",
        "c1511-list": "Complete `static long long solve(const struct node *head)`. The supplied `main` builds and later frees the list; `solve` must inspect it without changing ownership.",
        "c1511-text": "Complete `static long long solve(const char *s)`. The supplied `main` reads one line, removes its trailing newline, and prints the returned value.",
        "c1511-logic": "Complete `static long long solve(int a, int b, int c)`. The supplied `main` reads the three inputs and prints the returned value.",
        "c1511-grid": "Complete `static long long solve(const int *a, int rows, int columns)`. The grid is stored in row-major order, so cell `(r, c)` is `a[r * columns + c]`.",
        "c1511-record": "Complete `static long long solve(const struct record *a, int n)`. The supplied `main` reads the records and prints the returned value.",
        "c1511-system": "Complete the marked command loop and dynamic record table in `main`. This is a whole-program task; the starter provides only the data definition and includes.",
        "c1521-bits": "Complete `static uint32_t solve(uint32_t x, uint32_t y, unsigned k)`. The supplied `main` reads the values and prints the returned word in the required format.",
        "c1521-mips": "Complete the `solve` label only. It receives the array address in `$a0` and its length in `$a1`, and must return the result in `$v0`; the supplied `main` handles all syscalls.",
        "c1521-file": "Complete `static long long solve(const unsigned char *data, size_t n)`. The supplied `main` already opens the named file, reads every byte, closes it, and frees the buffer.",
        "c1521-unicode": "Complete `static long long solve(uint32_t cp)`. The supplied `main` reads the hexadecimal code point and prints the returned value.",
        "c1521-tree": "Complete `static int walk(const char *path, int depth, struct summary *s)`. The supplied `main` initialises the summary and prints the field needed by this question.",
        "c1521-thread": "Complete `static void *worker(void *arg)`. The supplied `main` reads the array, creates and joins exactly three threads, destroys the mutex, and prints the merged total.",
        "c1521-pipeline": "Complete the marked child-process branch. The supplied code already reads the array, creates the pipe, forks, receives one `long long`, waits for the child, and prints the result.",
    }
    return instructions[prefix]


def _prompt(question: AuthoredQuestion, first_stdout: str) -> str:
    filename = _slug_source(question.id, question.extension)
    task = question.definition or question.requirements
    return f"""# {question.title}

## Task

{task}

## Background

{question.background}

## Requirements

{question.requirements}

## Starter code

{_starter_instructions(question)}

## Examples

{_example_text(question.cases[0], first_stdout)}

## Implementation notes

{question.implementation_notes}

## Submission

Submit `{filename}` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
"""


def _solution(question: AuthoredQuestion, first_stdout: str) -> str:
    numbered = "\n".join(f"{index}. {step}" for index, step in enumerate(question.steps, start=1))
    return f"""# {question.title} — worked solution

## Idea in one sentence

{question.idea}

## Exact rule

{question.definition or question.requirements}

## Approach

{question.idea} Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

{numbered}

## Worked example

{_example_text(question.cases[0], first_stdout)}

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

{question.correctness}

## Complexity

{question.complexity}

## Common pitfalls

{question.pitfalls}

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
"""


def _emit(question: AuthoredQuestion, *, refresh: bool = False) -> bool:
    course_root = BANK_ROOT / question.course.lower()
    directory = course_root / "questions" / question.id
    if directory.exists() and not refresh:
        return False
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "starter").mkdir(exist_ok=True)
    (directory / "reference").mkdir(exist_ok=True)
    filename = _slug_source(question.id, question.extension)
    (directory / "starter" / filename).write_text(question.starter, encoding="utf-8")
    (directory / "reference" / filename).write_text(question.reference, encoding="utf-8")

    test_specs: list[dict[str, Any]] = []
    expected_outputs: list[tuple[str, str, int]] = []
    for case in question.cases:
        stdout, stderr, exit_code = question.oracle(case)
        expected_outputs.append((stdout, stderr, exit_code))
        fixtures: list[dict[str, str]] = []
        for source_name, target_name, content in case.fixtures:
            source = directory / "tests" / source_name
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_bytes(content)
            fixtures.append({"source": f"tests/{source_name}", "path": target_name})
        executable = _slug_source(question.id, "")
        argv = (
            ["mipsy", filename, *case.args]
            if question.kind == "mips_program"
            else [f"./{executable}", *case.args]
        )
        test: dict[str, Any] = {
            "id": case.id,
            "argv": argv,
            "stdin": case.stdin,
            "expected_stdout": stdout,
            "expected_stderr": stderr,
            "expected_exit": exit_code,
        }
        if question.course == "COMP1521":
            test["timeout_ms"] = 3000
        if fixtures:
            test["fixtures"] = fixtures
        test_specs.append(test)

    points, pass_points = _points(question.slot)
    public_points = pass_points
    raw = {
        "schema_version": 1,
        "id": question.id,
        "title": question.title,
        "kind": question.kind,
        "difficulty": question.difficulty,
        "track": question.track,
        "tags": list(question.tags),
        "weeks": list(question.weeks),
        "slots": [question.slot],
        "estimated_minutes": question.minutes,
        "points": points,
        "pass_points": pass_points,
        "prompt": "prompt.md",
        "solution": "solution.md",
        "starter_files": [f"starter/{filename}"],
        "submission_files": [filename],
        "build": {
            "argv": (
                []
                if question.kind == "mips_program"
                else [
                    "dcc" if question.course == "COMP1511" else "gcc",
                    *([] if question.course == "COMP1511" else ["-std=c11", "-Wall", "-Wextra"]),
                    *question.build_flags,
                    "-Werror",
                    filename,
                    "-o",
                    _slug_source(question.id, ""),
                ]
            )
        },
        "test_groups": [
            {
                "id": "public",
                "visibility": "public",
                "points": public_points,
                "tests": test_specs[:2],
            },
            {
                "id": "marking",
                "visibility": "after_finish",
                "points": points - public_points,
                "tests": test_specs[2:],
            },
        ],
    }
    first_stdout = expected_outputs[0][0]
    (directory / "question.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (directory / "prompt.md").write_text(_prompt(question, first_stdout), encoding="utf-8")
    (directory / "solution.md").write_text(_solution(question, first_stdout), encoding="utf-8")
    return True


def _sequence_input(values: Sequence[int]) -> str:
    tail = " ".join(str(value) for value in values)
    return f"{len(values)}\n{tail}\n" if values else "0\n"


SEQUENCE_CASES = (
    Case("mixed", stdin=_sequence_input((3, -1, -1, 4, 0, -2))),
    Case("empty", stdin=_sequence_input(())),
    Case("single", stdin=_sequence_input((5,))),
    Case("boundary", stdin=_sequence_input((0, 0, 1, -1, 2, -2))),
    Case("trend", stdin=_sequence_input((1, 2, 3, 2, 2, 5, 4))),
)


def _values(case: Case) -> list[int]:
    tokens = [int(token) for token in case.stdin.split()]
    return tokens[1 : 1 + tokens[0]]


def _sign(value: int) -> int:
    return (value > 0) - (value < 0)


def _longest(values: Sequence[int], relation: Callable[[int, int], bool]) -> int:
    if not values:
        return 0
    best = current = 1
    for left, right in zip(values, values[1:], strict=False):
        current = current + 1 if relation(left, right) else 1
        best = max(best, current)
    return best


SEQUENCE_OPERATIONS: tuple[tuple[str, str, str, Callable[[list[int]], int], str], ...] = (
    (
        "positive-total",
        "Solar Surplus Total",
        "a community battery log",
        lambda a: sum(x for x in a if x > 0),
        "long long result=0; for(int i=0;i<n;i++) if(a[i]>0) result+=a[i]; return result;",
    ),
    (
        "negative-count",
        "Freezer Alarm Count",
        "a cold-chain sensor feed",
        lambda a: sum(x < 0 for x in a),
        "long long result=0; for(int i=0;i<n;i++) if(a[i]<0) result++; return result;",
    ),
    (
        "even-count",
        "Even Platform Codes",
        "a railway platform audit",
        lambda a: sum(x % 2 == 0 for x in a),
        "long long result=0; for(int i=0;i<n;i++) if(a[i]%2==0) result++; return result;",
    ),
    (
        "peak-count",
        "Ridge Station Peaks",
        "a mountain weather transect",
        lambda a: sum(a[i] > a[i - 1] and a[i] > a[i + 1] for i in range(1, len(a) - 1)),
        "long long result=0; for(int i=1;i+1<n;i++) if(a[i]>a[i-1]&&a[i]>a[i+1]) result++; return result;",
    ),
    (
        "valley-count",
        "River Gauge Valleys",
        "a flood-monitoring transect",
        lambda a: sum(a[i] < a[i - 1] and a[i] < a[i + 1] for i in range(1, len(a) - 1)),
        "long long result=0; for(int i=1;i+1<n;i++) if(a[i]<a[i-1]&&a[i]<a[i+1]) result++; return result;",
    ),
    (
        "sign-change-count",
        "Pressure Sign Changes",
        "a laboratory pressure series",
        lambda a: sum(
            _sign(x) and _sign(y) and _sign(x) != _sign(y) for x, y in zip(a, a[1:], strict=False)
        ),
        "long long result=0; for(int i=1;i<n;i++) if(a[i-1]!=0&&a[i]!=0&&((a[i-1]<0)!=(a[i]<0))) result++; return result;",
    ),
    (
        "equal-neighbours",
        "Repeated Tag Neighbours",
        "a wildlife tag stream",
        lambda a: sum(x == y for x, y in zip(a, a[1:], strict=False)),
        "long long result=0; for(int i=1;i<n;i++) if(a[i]==a[i-1]) result++; return result;",
    ),
    (
        "rising-edges",
        "Ascending Lift Segments",
        "a building lift trace",
        lambda a: sum(y > x for x, y in zip(a, a[1:], strict=False)),
        "long long result=0; for(int i=1;i<n;i++) if(a[i]>a[i-1]) result++; return result;",
    ),
    (
        "alternating-total",
        "Alternating Drone Payload",
        "a drone loading manifest",
        lambda a: sum(x if i % 2 == 0 else -x for i, x in enumerate(a)),
        "long long result=0; for(int i=0;i<n;i++) result+=(i%2==0?a[i]:-a[i]); return result;",
    ),
    (
        "largest-magnitude",
        "Largest Seismic Magnitude",
        "a signed seismometer trace",
        lambda a: max((abs(x) for x in a), default=0),
        "long long result=0; for(int i=0;i<n;i++){long long x=a[i]; if(x<0)x=-x; if(x>result)result=x;} return result;",
    ),
    (
        "range-width",
        "Habitat Range Width",
        "a habitat elevation survey",
        lambda a: max(a) - min(a) if a else 0,
        "if(n==0)return 0; int lo=a[0],hi=a[0]; for(int i=1;i<n;i++){if(a[i]<lo)lo=a[i]; if(a[i]>hi)hi=a[i];} return (long long)hi-lo;",
    ),
    (
        "first-maximum",
        "First Busiest Gate",
        "an event gate counter",
        lambda a: a.index(max(a)) if a else -1,
        "if(n==0)return -1; int at=0; for(int i=1;i<n;i++)if(a[i]>a[at])at=i; return at;",
    ),
    (
        "last-minimum",
        "Last Lowest Reservoir",
        "a reservoir level survey",
        lambda a: len(a) - 1 - a[::-1].index(min(a)) if a else -1,
        "if(n==0)return -1; int at=0; for(int i=1;i<n;i++)if(a[i]<=a[at])at=i; return at;",
    ),
    (
        "longest-equal-run",
        "Longest Stable Voltage Run",
        "an electronics bench log",
        lambda a: _longest(a, lambda x, y: x == y),
        "if(n==0)return 0; int best=1,run=1; for(int i=1;i<n;i++){run=a[i]==a[i-1]?run+1:1; if(run>best)best=run;} return best;",
    ),
    (
        "longest-climb",
        "Longest Nondecreasing Trail",
        "a hiking trail profile",
        lambda a: _longest(a, lambda x, y: y >= x),
        "if(n==0)return 0; int best=1,run=1; for(int i=1;i<n;i++){run=a[i]>=a[i-1]?run+1:1; if(run>best)best=run;} return best;",
    ),
    (
        "distinct-count",
        "Distinct Specimen Labels",
        "a specimen label batch",
        lambda a: len(set(a)),
        "long long result=0; for(int i=0;i<n;i++){int seen=0; for(int j=0;j<i;j++)if(a[j]==a[i])seen=1; if(!seen)result++;} return result;",
    ),
    (
        "safe-prefix-count",
        "Solvent-Safe Prefixes",
        "a cumulative solvent ledger",
        lambda a: sum(total >= 0 for total in _prefixes(a)),
        "long long total=0,result=0; for(int i=0;i<n;i++){total+=a[i]; if(total>=0)result++;} return result;",
    ),
    (
        "adjacent-distance",
        "Robot Route Distance",
        "a one-dimensional robot route",
        lambda a: sum(abs(y - x) for x, y in zip(a, a[1:], strict=False)),
        "long long result=0; for(int i=1;i<n;i++){long long d=(long long)a[i]-a[i-1]; result+=d<0?-d:d;} return result;",
    ),
    (
        "weighted-checksum",
        "Archive Position Checksum",
        "a numbered archive shelf",
        lambda a: sum((i + 1) * x for i, x in enumerate(a)),
        "long long result=0; for(int i=0;i<n;i++)result+=(long long)(i+1)*a[i]; return result;",
    ),
    (
        "inversion-count",
        "Out-of-Order Seed Pairs",
        "a seed-sorting trial",
        lambda a: sum(a[i] > a[j] for i in range(len(a)) for j in range(i + 1, len(a))),
        "long long result=0; for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(a[i]>a[j])result++; return result;",
    ),
)

SEQUENCE_DEFINITIONS = {
    "positive-total": "Sum only values strictly greater than zero; return 0 for an empty array.",
    "negative-count": "Count elements strictly less than zero; zero is not negative.",
    "even-count": "Count elements whose remainder modulo 2 is zero, including zero and negative evens.",
    "peak-count": "Count interior indices `i` where `a[i] > a[i-1]` and `a[i] > a[i+1]`; endpoints never count.",
    "valley-count": "Count interior indices `i` where `a[i] < a[i-1]` and `a[i] < a[i+1]`; comparisons are strict.",
    "sign-change-count": "Count adjacent pairs with one strictly negative and one strictly positive value; pairs containing zero do not count.",
    "equal-neighbours": "Count adjacent index pairs `(i-1, i)` whose two values are equal.",
    "rising-edges": "Count adjacent pairs where the later value is strictly greater than the earlier value.",
    "alternating-total": "Compute `a[0] - a[1] + a[2] - a[3] + ...`.",
    "largest-magnitude": "Return the largest absolute element value, or 0 when the array is empty.",
    "range-width": "Return `maximum - minimum`, or 0 when the array is empty.",
    "first-maximum": "Return the zero-based index of the first maximum, or -1 for an empty array.",
    "last-minimum": "Return the zero-based index of the last minimum, or -1 for an empty array.",
    "longest-equal-run": "Return the maximum length of a contiguous run of equal values, or 0 for empty input.",
    "longest-climb": "Return the maximum length of a contiguous nondecreasing run (`next >= current`).",
    "distinct-count": "Count distinct integer values; repeated occurrences contribute only once.",
    "safe-prefix-count": "Count prefixes whose cumulative sum from index 0 is greater than or equal to zero.",
    "adjacent-distance": "Sum `abs(a[i] - a[i-1])` over all adjacent pairs.",
    "weighted-checksum": "Compute `sum((i + 1) * a[i])` using one-based position weights.",
    "inversion-count": "Count pairs `i < j` for which `a[i] > a[j]`.",
}


def _prefixes(values: Sequence[int]) -> list[int]:
    result: list[int] = []
    total = 0
    for value in values:
        total += value
        result.append(total)
    return result


def _sequence_source(body: str, *, starter: bool) -> str:
    solve = (
        "static long long solve(const int *a,int n){(void)a;(void)n;return 0;}"
        if starter
        else f"static long long solve(const int *a,int n){{{body}}}"
    )
    return f"""#include <stdio.h>
{solve}
int main(void){{
    int n;
    int values[100];
    if(scanf("%d",&n)!=1||n<0||n>100)return 1;
    for(int i=0;i<n;i++)if(scanf("%d",&values[i])!=1)return 1;
    printf("result: %lld\\n",solve(values,n));
    return 0;
}}
"""


def _sequence_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 5)
    for index, (key, title, setting, oracle, body) in enumerate(SEQUENCE_OPERATIONS, start=1):
        slot = "array_hurdle" if index <= 16 else "medium"
        difficulty = difficulties[index - 1]
        tags = ["arrays-1d", "loops", "functions"]
        if key in {"distinct-count", "inversion-count"}:
            tags.append("testing")
        if key in {"first-maximum", "last-minimum"}:
            tags.append("pointers")
        if key in {"sign-change-count", "safe-prefix-count"}:
            tags.append("conditionals")
        question_id = f"c1511-array-{index:03d}"

        def run(case: Case, operation: Callable[[list[int]], int] = oracle) -> tuple[str, str, int]:
            return f"result: {operation(_values(case))}\n", "", 0

        yield AuthoredQuestion(
            id=question_id,
            title=title,
            course="COMP1511",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 4 else "normal",
            tags=tuple(tags),
            weeks=(4, 5) if slot == "medium" else (4,),
            slot=slot,
            minutes=12 + difficulty * 4,
            background=f"The data comes from {setting} and is stored as a bounded integer array. The array order is significant whenever the task refers to positions or neighbours.",
            requirements="Read `n` (0 to 100), followed by `n` signed integers. Print the computed value as `result: X` followed by a newline. The task rule states the result for an empty array whenever `n = 0` is valid.",
            implementation_notes="Use the supplied array and helper function. Do not sort or alter the input unless the task explicitly depends on ordering. All supplied arithmetic fits in `long long`.",
            idea=f"Scan the array while maintaining exactly the state needed for {title.lower()}.",
            steps=(
                "Read and validate `n`, then store exactly `n` values.",
                "Initialise the metric's neutral state, including any previous-item state.",
                "Visit every required index once (or every ordered pair for the pair-count task).",
                "Print the final `long long` result with the required label.",
            ),
            correctness="The helper examines precisely the indices named by the definition. Its maintained state equals the metric for the processed prefix; extending by one value adds exactly that value's contribution. Therefore the final state equals the metric for the complete array.",
            complexity="The scan uses `O(n)` time and `O(n)` input storage; the distinct/inversion variants intentionally use `O(n^2)` time. Auxiliary state is `O(1)`.",
            pitfalls="Do not read neighbours at the endpoints, change the first/last tie rule, or treat zero as positive/negative unless stated. Handle `n == 0` before reading `values[0]`.",
            starter=_sequence_source(body, starter=True),
            reference=_sequence_source(body, starter=False),
            cases=SEQUENCE_CASES,
            oracle=run,
            definition=SEQUENCE_DEFINITIONS[key],
        )


LIST_CASES = (
    Case("mixed", args=("3", "-1", "-1", "4", "0", "-2")),
    Case("empty", args=()),
    Case("single", args=("5",)),
    Case("ordered", args=("1", "2", "3", "4", "5")),
    Case("ties", args=("7", "7", "2", "7", "2", "2")),
)


def _arg_values(case: Case) -> list[int]:
    return [int(value) for value in case.args]


LIST_OPERATIONS: tuple[tuple[str, str, Callable[[list[int]], int], str, bool], ...] = (
    (
        "total",
        "Field Sample Chain Total",
        sum,
        "long long r=0;for(;h;h=h->next)r+=h->value;return r;",
        False,
    ),
    (
        "alternating",
        "Alternating Buoy Chain",
        lambda a: sum(x if i % 2 == 0 else -x for i, x in enumerate(a)),
        "long long r=0;int i=0;for(;h;h=h->next,i++)r+=i%2==0?h->value:-h->value;return r;",
        False,
    ),
    (
        "rises",
        "Rising Relay Links",
        lambda a: sum(y > x for x, y in zip(a, a[1:], strict=False)),
        "long long r=0;for(;h&&h->next;h=h->next)if(h->next->value>h->value)r++;return r;",
        False,
    ),
    (
        "even",
        "Even Cargo Nodes",
        lambda a: sum(x % 2 == 0 for x in a),
        "long long r=0;for(;h;h=h->next)if(h->value%2==0)r++;return r;",
        False,
    ),
    (
        "first-max",
        "First Maximum Checkpoint",
        lambda a: a.index(max(a)) if a else -1,
        "if(!h)return -1;long long at=0,best_at=0;int best=h->value;for(;h;h=h->next,at++)if(h->value>best){best=h->value;best_at=at;}return best_at;",
        False,
    ),
    (
        "equal-run",
        "Longest Identical Wagon Run",
        lambda a: _longest(a, lambda x, y: x == y),
        "if(!h)return 0;long long best=1,run=1;for(;h->next;h=h->next){run=h->value==h->next->value?run+1:1;if(run>best)best=run;}return best;",
        False,
    ),
    ("recursive-total", "Recursive Reef Chain Total", sum, "return recursive_total(h);", True),
    (
        "recursive-negative",
        "Recursive Fault Node Count",
        lambda a: sum(x < 0 for x in a),
        "return recursive_negative(h);",
        True,
    ),
    (
        "palindrome",
        "Symmetric Beacon Chain",
        lambda a: int(a == a[::-1]),
        "int a[100],n=0;for(;h&&n<100;h=h->next)a[n++]=h->value;for(int i=0;i<n/2;i++)if(a[i]!=a[n-1-i])return 0;return 1;",
        False,
    ),
    (
        "weighted",
        "Distance-Weighted Supply Chain",
        lambda a: sum((i + 1) * x for i, x in enumerate(a)),
        "long long r=0,i=1;for(;h;h=h->next,i++)r+=i*h->value;return r;",
        False,
    ),
    (
        "local-peaks",
        "Peak Signal Nodes",
        lambda a: sum(a[i] > a[i - 1] and a[i] > a[i + 1] for i in range(1, len(a) - 1)),
        "long long r=0;if(!h)return 0;for(;h->next&&h->next->next;h=h->next)if(h->next->value>h->value&&h->next->value>h->next->next->value)r++;return r;",
        False,
    ),
    (
        "end-difference",
        "Chain Endpoint Difference",
        lambda a: abs(a[0] - a[-1]) if a else 0,
        "if(!h)return 0;int first=h->value,last=first;for(;h;h=h->next)last=h->value;long long d=(long long)first-last;return d<0?-d:d;",
        False,
    ),
)

LIST_DEFINITIONS = {
    "total": "Return the sum of every node value, with the empty-list result 0.",
    "alternating": "Compute `node[0] - node[1] + node[2] - ...` in list order.",
    "rises": "Count links whose next node has a strictly greater value.",
    "even": "Count nodes containing an even integer, including zero and negative evens.",
    "first-max": "Return the zero-based position of the first maximum node, or -1 for an empty list.",
    "equal-run": "Return the longest contiguous run of equal node values, or 0 for an empty list.",
    "recursive-total": "Recursively return `head->value + total(head->next)`, with `total(NULL) = 0`.",
    "recursive-negative": "Recursively count nodes whose value is strictly negative.",
    "palindrome": "Return 1 exactly when the node-value sequence reads the same forwards and backwards; the empty list counts as a palindrome.",
    "weighted": "Compute `sum((position + 1) * value)` in list order.",
    "local-peaks": "Count non-endpoint nodes whose value is strictly greater than both adjacent node values.",
    "end-difference": "Return the absolute difference between the first and last node values, or 0 for an empty list.",
}


def _list_source(body: str, *, recursive: bool, starter: bool) -> str:
    helpers = ""
    if recursive:
        helpers = """static long long recursive_total(const struct node*h){return h?h->value+recursive_total(h->next):0;}
static long long recursive_negative(const struct node*h){return h?(h->value<0)+recursive_negative(h->next):0;}
"""
    solve = (
        "static long long solve(const struct node*h){(void)h;return 0;}"
        if starter
        else f"static long long solve(const struct node*h){{{body}}}"
    )
    return f"""#include <stdio.h>
#include <stdlib.h>
struct node{{int value;struct node*next;}};
{helpers}{solve}
int main(int argc,char**argv){{
    struct node*head=NULL;struct node**tail=&head;
    for(int i=1;i<argc;i++){{struct node*n=malloc(sizeof*n);if(!n)return 1;n->value=atoi(argv[i]);n->next=NULL;*tail=n;tail=&n->next;}}
    printf("result: %lld\\n",solve(head));
    while(head){{struct node*next=head->next;free(head);head=next;}}
    return 0;
}}
"""


def _list_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3)
    for index, (key, title, operation, body, recursive) in enumerate(LIST_OPERATIONS, start=1):
        difficulty = difficulties[index - 1]
        tags = ["linked-lists", "pointers", "dynamic-memory", "functions", "loops"]
        if recursive:
            tags.append("recursion")

        def run(case: Case, op: Callable[[list[int]], int] = operation) -> tuple[str, str, int]:
            return f"result: {op(_arg_values(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1511-list-{index:03d}",
            title=title,
            course="COMP1511",
            kind="c_function",
            difficulty=difficulty,
            track="challenge" if difficulty >= 3 else "normal",
            tags=tuple(tags),
            weeks=(6, 7),
            slot="list_hurdle",
            minutes=14 + difficulty * 4,
            background="A linked chain stores readings in arrival order. The supplied `main` owns the nodes and frees the complete chain after `solve` returns.",
            requirements="Each command-line integer becomes one list node in the same order. With no arguments, `head` is `NULL`. Return the required value from `solve`; the supplied `main` prints it as `result: X`.",
            implementation_notes="Do not change `main` or print inside `solve`. Preserve every `next` link. Recursive variants should give the empty-list base case before accessing a node.",
            idea=f"Traverse the chain in order and maintain the minimal state for {title.lower()}.",
            steps=(
                "Handle `head == NULL` using the documented neutral result.",
                "Save any current/next values needed by the metric before advancing.",
                "Update the running result exactly once per eligible node or adjacent pair.",
                "Return the scalar result; leave allocation and printing to the harness.",
            ),
            correctness="After each traversal step, the accumulator equals the required metric for the consumed prefix. The update adds exactly the current node's or pair's contribution, and termination occurs after the final node, so the returned value is exact.",
            complexity="The list is traversed in `O(n)` time with `O(1)` iterative state. Recursive variants use `O(n)` call-stack space.",
            pitfalls="Do not dereference `NULL`, advance twice, prefer the last maximum when the first is required, or free nodes inside the metric. An empty argument list is a real test case.",
            starter=_list_source(body, recursive=recursive, starter=True),
            reference=_list_source(body, recursive=recursive, starter=False),
            cases=LIST_CASES,
            oracle=run,
            definition=LIST_DEFINITIONS[key],
        )


STRING_CASES = (
    Case("mixed", stdin="A1 beta\n"),
    Case("empty-line", stdin="\n"),
    Case("repeats", stdin="bookkeeper\n"),
    Case("brackets", stdin="((a)b)\n"),
    Case("spaces", stdin="  mixed CASE 42  \n"),
)


def _line(case: Case) -> str:
    return case.stdin.rstrip("\n")


def _word_count(text: str) -> int:
    return len(text.split())


def _longest_word(text: str) -> int:
    return max((len(word) for word in text.split()), default=0)


def _alnum_palindrome(text: str) -> int:
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return int(cleaned == cleaned[::-1])


STRING_OPERATIONS: tuple[tuple[str, str, Callable[[str], int], str], ...] = (
    (
        "vowels",
        "Vowels in a Radio Transcript",
        lambda s: sum(ch.lower() in "aeiou" for ch in s),
        'long long r=0;for(int i=0;s[i];i++)if(strchr("aeiouAEIOU",s[i]))r++;return r;',
    ),
    (
        "digits",
        "Digits in a Sample Label",
        lambda s: sum(ch.isdigit() for ch in s),
        "long long r=0;for(int i=0;s[i];i++)if(isdigit((unsigned char)s[i]))r++;return r;",
    ),
    (
        "words",
        "Words in a Dispatch Message",
        _word_count,
        "long long r=0;int in=0;for(int i=0;s[i];i++){if(isspace((unsigned char)s[i]))in=0;else if(!in){in=1;r++;}}return r;",
    ),
    (
        "uppercase",
        "Uppercase Map Markers",
        lambda s: sum(ch.isupper() for ch in s),
        "long long r=0;for(int i=0;s[i];i++)if(isupper((unsigned char)s[i]))r++;return r;",
    ),
    (
        "lowercase",
        "Lowercase Gene Symbols",
        lambda s: sum(ch.islower() for ch in s),
        "long long r=0;for(int i=0;s[i];i++)if(islower((unsigned char)s[i]))r++;return r;",
    ),
    (
        "adjacent-repeat",
        "Repeated Keyboard Strokes",
        lambda s: sum(a == b for a, b in zip(s, s[1:], strict=False)),
        "long long r=0;for(int i=1;s[i];i++)if(s[i]==s[i-1])r++;return r;",
    ),
    (
        "runs",
        "Character Runs in a Barcode Note",
        lambda s: 0 if not s else 1 + sum(a != b for a, b in zip(s, s[1:], strict=False)),
        "if(!s[0])return 0;long long r=1;for(int i=1;s[i];i++)if(s[i]!=s[i-1])r++;return r;",
    ),
    (
        "max-depth",
        "Maximum Bracket Nesting",
        lambda s: _max_depth(s),
        "long long depth=0,best=0;for(int i=0;s[i];i++){if(s[i]=='('){depth++;if(depth>best)best=depth;}else if(s[i]==')'){depth--;if(depth<0)return -1;}}return depth==0?best:-1;",
    ),
    (
        "balanced",
        "Balanced Console Parentheses",
        lambda s: int(_max_depth(s) >= 0),
        "long long depth=0;for(int i=0;s[i];i++){if(s[i]=='(')depth++;else if(s[i]==')'&&--depth<0)return 0;}return depth==0;",
    ),
    (
        "letter-checksum",
        "Case-Folded Letter Checksum",
        lambda s: sum(ord(ch.lower()) - 96 for ch in s if ch.isalpha()),
        "long long r=0;for(int i=0;s[i];i++)if(isalpha((unsigned char)s[i]))r+=tolower((unsigned char)s[i])-'a'+1;return r;",
    ),
    (
        "case-switches",
        "Case Transition Counter",
        lambda s: _case_switches(s),
        "long long r=0;int prev=0;for(int i=0;s[i];i++){int now=isupper((unsigned char)s[i])?1:islower((unsigned char)s[i])?2:0;if(now&&prev&&now!=prev)r++;if(now)prev=now;}return r;",
    ),
    (
        "space-groups",
        "Whitespace Group Counter",
        lambda s: _space_groups(s),
        "long long r=0;int in=0;for(int i=0;s[i];i++){int now=isspace((unsigned char)s[i]);if(now&&!in)r++;in=now;}return r;",
    ),
    (
        "longest-word",
        "Longest Emergency Call Word",
        _longest_word,
        "long long best=0,run=0;for(int i=0;;i++){if(s[i]&&!isspace((unsigned char)s[i]))run++;else{if(run>best)best=run;run=0;if(!s[i])break;}}return best;",
    ),
    (
        "first-digit",
        "First Numeric Field Position",
        lambda s: next((i for i, ch in enumerate(s) if ch.isdigit()), -1),
        "for(int i=0;s[i];i++)if(isdigit((unsigned char)s[i]))return i;return -1;",
    ),
    (
        "palindrome",
        "Normalised Identifier Palindrome",
        _alnum_palindrome,
        "char clean[256];int n=0;for(int i=0;s[i]&&n<255;i++)if(isalnum((unsigned char)s[i]))clean[n++]=(char)tolower((unsigned char)s[i]);for(int i=0;i<n/2;i++)if(clean[i]!=clean[n-1-i])return 0;return 1;",
    ),
)

STRING_DEFINITIONS = {
    "vowels": "Count ASCII letters `a`, `e`, `i`, `o`, or `u`, ignoring case.",
    "digits": "Count ASCII decimal characters from `0` through `9`.",
    "words": "Count maximal non-whitespace runs; any ASCII whitespace separates words.",
    "uppercase": "Count uppercase ASCII letters.",
    "lowercase": "Count lowercase ASCII letters.",
    "adjacent-repeat": "Count adjacent character pairs that contain the same byte.",
    "runs": "Count maximal contiguous runs of identical characters; the empty line has 0 runs.",
    "max-depth": "Return the maximum parenthesis nesting depth, or -1 if any prefix closes below zero or the final depth is nonzero.",
    "balanced": "Return 1 for a balanced parenthesis sequence and 0 otherwise; non-parenthesis characters are ignored.",
    "letter-checksum": "For each ASCII letter add its case-insensitive alphabet position (`a=1` through `z=26`).",
    "case-switches": "Ignore nonletters, then count transitions between uppercase and lowercase among consecutive remaining letters.",
    "space-groups": "Count maximal contiguous groups of whitespace characters.",
    "longest-word": "Return the maximum length of a maximal non-whitespace word, or 0 when there are none.",
    "first-digit": "Return the zero-based index of the first decimal digit, or -1 when no digit occurs.",
    "palindrome": "Remove non-alphanumeric characters, fold letters to lowercase, then return 1 iff the result is a palindrome.",
}


def _max_depth(text: str) -> int:
    depth = best = 0
    for char in text:
        if char == "(":
            depth += 1
            best = max(best, depth)
        elif char == ")":
            depth -= 1
            if depth < 0:
                return -1
    return best if depth == 0 else -1


def _case_switches(text: str) -> int:
    states = ["upper" if char.isupper() else "lower" for char in text if char.isalpha()]
    return sum(left != right for left, right in zip(states, states[1:], strict=False))


def _space_groups(text: str) -> int:
    return len(re.findall(r"\s+", text))


def _string_source(body: str, *, starter: bool) -> str:
    solve = (
        "static long long solve(const char*s){(void)s;return 0;}"
        if starter
        else f"static long long solve(const char*s){{{body}}}"
    )
    return f"""#include <ctype.h>
#include <stdio.h>
#include <string.h>
{solve}
int main(void){{char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\\n")]='\\0';printf("result: %lld\\n",solve(line));return 0;}}
"""


def _string_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (1, 1, 1, 1, 2, 2, 2, 3, 3, 2, 3, 2, 3, 4, 4)
    for index, (key, title, operation, body) in enumerate(STRING_OPERATIONS, start=1):
        slot = "short" if index <= 12 else "medium"
        difficulty = difficulties[index - 1]

        def run(case: Case, op: Callable[[str], int] = operation) -> tuple[str, str, int]:
            return f"result: {op(_line(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1511-text-{index:03d}",
            title=title,
            course="COMP1511",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 3 else "normal",
            tags=("strings", "char-streams", "loops", "functions", "conditionals"),
            weeks=(3, 5),
            slot=slot,
            minutes=10 + difficulty * 4,
            background="A line-oriented tool must summarise human-readable text. The complete line, including spaces, is meaningful.",
            requirements="Read one line of at most 255 characters, excluding the final newline from the calculation. Print `result: X` and a newline. Character classification is ASCII for these tests.",
            implementation_notes="Use `fgets`, remove at most one trailing newline, and cast to `unsigned char` before calling `<ctype.h>` functions.",
            idea=f"Scan the line from left to right and retain only the state needed for {title.lower()}.",
            steps=(
                "Read the whole line and remove its trailing newline.",
                "Initialise counters plus any previous-character or nesting state.",
                "Classify each character once and update the state according to the exact rule.",
                "Return the scalar result and print it once.",
            ),
            correctness="The scan classifies every character exactly once. Its counters and previous-state variables describe the processed prefix, and the update matches the definition for the next character. Thus the returned result describes the full line.",
            complexity="The algorithm uses `O(n)` time and `O(1)` auxiliary space, except the normalised-palindrome variant's `O(n)` buffer.",
            pitfalls='Do not use `scanf("%s")`, count the newline, pass a negative plain `char` to `<ctype.h>`, or forget to validate unmatched closing parentheses.',
            starter=_string_source(body, starter=True),
            reference=_string_source(body, starter=False),
            cases=STRING_CASES,
            oracle=run,
            definition=STRING_DEFINITIONS[key],
        )


NUMERIC_CASES = (
    Case("mixed", stdin="-4 9 2\n"),
    Case("ascending", stdin="1 2 3\n"),
    Case("equal", stdin="5 5 5\n"),
    Case("boundary", stdin="0 -1 1\n"),
    Case("reverse", stdin="12 7 -3\n"),
)


def _triple(case: Case) -> tuple[int, int, int]:
    a, b, c = (int(value) for value in case.stdin.split())
    return a, b, c


def _triangle_code(values: tuple[int, int, int]) -> int:
    a, b, c = values
    if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
        return 0
    if a == b == c:
        return 3
    return 2 if len({a, b, c}) == 2 else 1


NUMERIC_OPERATIONS: tuple[
    tuple[str, str, Callable[[tuple[int, int, int]], int], str, tuple[str, ...]], ...
] = (
    (
        "median",
        "Median Calibration Reading",
        lambda v: sorted(v)[1],
        "if((a<=b&&b<=c)||(c<=b&&b<=a))return b;if((b<=a&&a<=c)||(c<=a&&a<=b))return a;return c;",
        ("conditionals", "io"),
    ),
    (
        "triangle",
        "Triangle Support Code",
        _triangle_code,
        "if(a<=0||b<=0||c<=0||a+b<=c||a+c<=b||b+c<=a)return 0;if(a==b&&b==c)return 3;if(a==b||b==c||a==c)return 2;return 1;",
        ("enums", "conditionals", "io"),
    ),
    (
        "clamp",
        "Bounded Pump Setting",
        lambda v: max(min(v[1], max(v[0], v[2])), min(v[0], v[2])),
        "int lo=a<c?a:c,hi=a>c?a:c;return b<lo?lo:b>hi?hi:b;",
        ("debugging", "conditionals", "functions"),
    ),
    (
        "largest-absolute",
        "Largest Absolute Offset",
        lambda v: max(abs(x) for x in v),
        "long long x=a<0?-(long long)a:a,y=b<0?-(long long)b:b,z=c<0?-(long long)c:c;return x>y?(x>z?x:z):(y>z?y:z);",
        ("conditionals", "functions"),
    ),
    (
        "distinct",
        "Distinct Channel Count",
        lambda v: len(set(v)),
        "return a==b&&b==c?1:(a==b||b==c||a==c?2:3);",
        ("conditionals", "testing"),
    ),
    (
        "progression",
        "Arithmetic Progression Check",
        lambda v: int(v[1] - v[0] == v[2] - v[1]),
        "return b-a==c-b;",
        ("conditionals", "functions"),
    ),
    (
        "sorted-code",
        "Three-Reading Order Code",
        lambda v: 1 if v[0] <= v[1] <= v[2] else -1 if v[0] >= v[1] >= v[2] else 0,
        "if(a<=b&&b<=c)return 1;if(a>=b&&b>=c)return -1;return 0;",
        ("enums", "conditionals"),
    ),
    (
        "closest-zero",
        "Closest Reading to Zero",
        lambda v: min(v, key=lambda x: (abs(x), x)),
        "int r=a;long long ar=a<0?-(long long)a:a,br=b<0?-(long long)b:b,cr=c<0?-(long long)c:c;if(br<ar||(br==ar&&b<r)){r=b;ar=br;}if(cr<ar||(cr==ar&&c<r))r=c;return r;",
        ("structs", "conditionals"),
    ),
    (
        "pair-spread",
        "Largest Pair Spread",
        lambda v: max(v) - min(v),
        "int lo=a,hi=a;if(b<lo)lo=b;if(c<lo)lo=c;if(b>hi)hi=b;if(c>hi)hi=c;return (long long)hi-lo;",
        ("debugging", "functions", "io"),
    ),
)

NUMERIC_DEFINITIONS = {
    "median": "Return the middle value after ordering the three inputs; repeated values are retained.",
    "triangle": "Return 0 for invalid sides; otherwise return 3 for equilateral, 2 for isosceles, and 1 for scalene.",
    "clamp": "Treat the first and third inputs as unordered inclusive bounds and clamp the second input between them.",
    "largest-absolute": "Return the largest absolute magnitude among the three signed inputs.",
    "distinct": "Return 1, 2, or 3 according to the number of distinct input values.",
    "progression": "Return 1 exactly when `b - a == c - b`, otherwise return 0.",
    "sorted-code": "Return 1 for nondecreasing order, -1 for nonincreasing order, and 0 otherwise; all-equal returns 1.",
    "closest-zero": "Return the value with smallest absolute magnitude; break a magnitude tie by choosing the smaller value.",
    "pair-spread": "Return the largest input minus the smallest input.",
}


def _numeric_source(body: str, *, starter: bool) -> str:
    solve = (
        "static long long solve(int a,int b,int c){(void)a;(void)b;(void)c;return 0;}"
        if starter
        else f"static long long solve(int a,int b,int c){{{body}}}"
    )
    return f'#include <stdio.h>\n{solve}\nint main(void){{int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\\n",solve(a,b,c));return 0;}}\n'


def _numeric_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (1, 1, 2, 2, 2, 2, 3, 3, 3)
    for index, (key, title, operation, body, extra_tags) in enumerate(
        NUMERIC_OPERATIONS, start=1
    ):
        difficulty = difficulties[index - 1]

        def run(
            case: Case, op: Callable[[tuple[int, int, int]], int] = operation
        ) -> tuple[str, str, int]:
            return f"result: {op(_triple(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1511-logic-{index:03d}",
            title=title,
            course="COMP1511",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 3 else "normal",
            tags=tuple(dict.fromkeys((*extra_tags, "conditionals"))),
            weeks=(1, 2, 3),
            slot="short",
            minutes=8 + difficulty * 4,
            background="A small control program receives three signed readings and must make one deterministic decision. Equality and signed boundary cases are intentional.",
            requirements="Read exactly three signed integers from standard input. Print the computed value as `result: X` followed by one newline.",
            implementation_notes="Use named intermediate values when that makes the tie rule visible. Do not rely on undefined signed overflow.",
            idea=f"Compare the three values in a fixed order to compute {title.lower()}.",
            steps=(
                "Read all three values and identify any ordering-independent bounds.",
                "Apply equality and validity rules before the general branches.",
                "Resolve ties using the order stated in the task.",
                "Print the resulting integer code.",
            ),
            correctness="The branch conditions partition all possible triples into the cases in the specification. Each branch returns the value defined for its case, so exactly one correct result is produced.",
            complexity="A constant number of comparisons uses `O(1)` time and `O(1)` space.",
            pitfalls="Test equal values, negative values, and values exactly on a branch boundary. Avoid chained C comparisons such as `a < b < c`.",
            starter=_numeric_source(body, starter=True),
            reference=_numeric_source(body, starter=False),
            cases=NUMERIC_CASES,
            oracle=run,
            definition=NUMERIC_DEFINITIONS[key],
        )


GRID_CASES = (
    Case("rectangle", stdin="2 3\n1 2 3\n4 5 6\n"),
    Case("empty", stdin="0 0\n"),
    Case("single", stdin="1 1\n5\n"),
    Case("signed", stdin="3 3\n1 -2 3\n4 0 -6\n7 8 9\n"),
    Case("ties", stdin="2 2\n2 2\n2 2\n"),
)


def _grid(case: Case) -> tuple[int, int, list[int]]:
    tokens = [int(x) for x in case.stdin.split()]
    r, c = tokens[:2]
    return r, c, tokens[2:]


def _border(g: tuple[int, int, list[int]]) -> int:
    r, c, a = g
    return sum(
        a[i * c + j] for i in range(r) for j in range(c) if i in {0, r - 1} or j in {0, c - 1}
    )


def _diag(g: tuple[int, int, list[int]]) -> int:
    r, c, a = g
    return sum(a[i * c + i] for i in range(min(r, c)))


def _row_index(g: tuple[int, int, list[int]]) -> int:
    r, c, a = g
    return max(range(r), key=lambda i: (sum(a[i * c : (i + 1) * c]), -i)) if r and c else -1


def _symmetric_mismatch(g: tuple[int, int, list[int]]) -> int:
    r, c, a = g
    return sum(a[i * c + j] != a[i * c + (c - 1 - j)] for i in range(r) for j in range(c // 2))


def _local_peaks(g: tuple[int, int, list[int]]) -> int:
    r, c, a = g
    result = 0
    for i in range(r):
        for j in range(c):
            neighbours = [
                a[x * c + y]
                for x, y in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
                if 0 <= x < r and 0 <= y < c
            ]
            result += bool(neighbours) and all(a[i * c + j] > x for x in neighbours)
    return result


def _zero_rows(g: tuple[int, int, list[int]]) -> int:
    r, c, a = g
    return sum(all(x == 0 for x in a[i * c : (i + 1) * c]) for i in range(r))


def _window(g: tuple[int, int, list[int]]) -> int:
    r, c, a = g
    return max(
        (
            a[i * c + j] + a[i * c + j + 1] + a[(i + 1) * c + j] + a[(i + 1) * c + j + 1]
            for i in range(r - 1)
            for j in range(c - 1)
        ),
        default=0,
    )


def _range_sum(g: tuple[int, int, list[int]]) -> int:
    return max(g[2]) - min(g[2]) if g[2] else 0


GRID_OPERATIONS = (
    (
        "border",
        "Coastal Grid Border Total",
        _border,
        "long long x=0;for(int i=0;i<r;i++)for(int j=0;j<c;j++)if(i==0||j==0||i==r-1||j==c-1)x+=a[i*c+j];return x;",
    ),
    (
        "diagonal",
        "Survey Main Diagonal",
        _diag,
        "long long x=0;for(int i=0;i<r&&i<c;i++)x+=a[i*c+i];return x;",
    ),
    (
        "row",
        "First Highest-Energy Row",
        _row_index,
        "if(r==0||c==0)return -1;long long best=0;for(int j=0;j<c;j++)best+=a[j];int at=0;for(int i=1;i<r;i++){long long x=0;for(int j=0;j<c;j++)x+=a[i*c+j];if(x>best){best=x;at=i;}}return at;",
    ),
    (
        "mirror",
        "Horizontal Mirror Mismatches",
        _symmetric_mismatch,
        "long long x=0;for(int i=0;i<r;i++)for(int j=0;j<c/2;j++)if(a[i*c+j]!=a[i*c+c-1-j])x++;return x;",
    ),
    (
        "peaks",
        "Four-Neighbour Terrain Peaks",
        _local_peaks,
        "long long x=0;for(int i=0;i<r;i++)for(int j=0;j<c;j++){int v=a[i*c+j],ok=(r*c>1);if(i&&a[(i-1)*c+j]>=v)ok=0;if(i+1<r&&a[(i+1)*c+j]>=v)ok=0;if(j&&a[i*c+j-1]>=v)ok=0;if(j+1<c&&a[i*c+j+1]>=v)ok=0;if(ok)x++;}return x;",
    ),
    (
        "zero-rows",
        "All-Zero Sensor Rows",
        _zero_rows,
        "long long x=0;for(int i=0;i<r;i++){int ok=1;for(int j=0;j<c;j++)if(a[i*c+j])ok=0;if(ok)x++;}return x;",
    ),
    (
        "window",
        "Maximum Two-by-Two Load",
        _window,
        "if(r<2||c<2)return 0;long long best=(long long)a[0]+a[1]+a[c]+a[c+1];for(int i=0;i+1<r;i++)for(int j=0;j+1<c;j++){long long x=(long long)a[i*c+j]+a[i*c+j+1]+a[(i+1)*c+j]+a[(i+1)*c+j+1];if(x>best)best=x;}return best;",
    ),
    (
        "range",
        "Grid Value Range",
        _range_sum,
        "if(r==0||c==0)return 0;int lo=a[0],hi=a[0];for(int i=1;i<r*c;i++){if(a[i]<lo)lo=a[i];if(a[i]>hi)hi=a[i];}return (long long)hi-lo;",
    ),
)

GRID_DEFINITIONS = {
    "border": "Sum cells in the first/last row or first/last column exactly once; empty grids return 0.",
    "diagonal": "Sum cells `(i, i)` for `0 <= i < min(rows, columns)`.",
    "row": "Return the first row index with greatest row sum, or -1 if either dimension is zero.",
    "mirror": "Count unequal horizontal mirror pairs, examining each pair only once.",
    "peaks": "Count cells strictly greater than every existing orthogonal neighbour; a neighbourless cell does not count.",
    "zero-rows": "Count rows for which every cell is zero.",
    "window": "Return the maximum sum of a contiguous 2-by-2 window, or 0 when no such window exists.",
    "range": "Return maximum cell minus minimum cell, or 0 for an empty grid.",
}


def _grid_source(body: str, *, starter: bool) -> str:
    solve = (
        "static long long solve(const int*a,int r,int c){(void)a;(void)r;(void)c;return 0;}"
        if starter
        else f"static long long solve(const int*a,int r,int c){{{body}}}"
    )
    return f'#include <stdio.h>\n{solve}\nint main(void){{int r,c,a[64];if(scanf("%d%d",&r,&c)!=2||r<0||c<0||r>8||c>8)return 1;for(int i=0;i<r*c;i++)if(scanf("%d",&a[i])!=1)return 1;printf("result: %lld\\n",solve(a,r,c));return 0;}}\n'


def _grid_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (3, 3, 4, 4, 4, 4, 5, 5)
    for index, (key, title, op, body) in enumerate(GRID_OPERATIONS, start=1):
        difficulty = difficulties[index - 1]

        def run(
            case: Case, operation: Callable[[tuple[int, int, list[int]]], int] = op
        ) -> tuple[str, str, int]:
            return f"result: {operation(_grid(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1511-grid-{index:03d}",
            title=title,
            course="COMP1511",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 4 else "normal",
            tags=("arrays-2d", "arrays-1d", "loops", "functions", "testing"),
            weeks=(4, 5),
            slot="medium",
            minutes=22 + difficulty * 4,
            background="A rectangular grid models a spatial survey. Rows and columns may differ, so every index calculation must use the supplied column count.",
            requirements="Read `rows columns` (each 0 to 8), then the grid in row-major order. Print the computed value as `result: X` followed by one newline.",
            implementation_notes="Store the grid in a bounded flat or two-dimensional array. Check dimensions before accessing the first cell or a neighbour/window.",
            idea=f"Visit exactly the cells participating in {title.lower()} and maintain one scalar result.",
            steps=(
                "Validate dimensions and read `rows * columns` values.",
                "Choose loop bounds that match the cells or windows in the definition.",
                "Update the result with each eligible cell exactly once.",
                "Return the neutral value for an empty or too-small grid and print once.",
            ),
            correctness="The nested loops enumerate every and only eligible grid position. Each update equals that position's contribution, so aggregation over all iterations yields the defined grid metric.",
            complexity="The algorithm uses `O(rows * columns)` time and stores at most 64 integers.",
            pitfalls="Do not assume a square grid, use `rows` as the row stride, or access neighbours/windows before proving they exist.",
            starter=_grid_source(body, starter=True),
            reference=_grid_source(body, starter=False),
            cases=GRID_CASES,
            oracle=run,
            definition=GRID_DEFINITIONS[key],
        )


RECORD_CASES = (
    Case("mixed", stdin="4\na 3\nb -1\nc 3\nd 8\n"),
    Case("empty", stdin="0\n"),
    Case("single", stdin="1\na 5\n"),
    Case("ordered", stdin="5\na 1\nb 2\nc 3\nd 4\ne 5\n"),
    Case("ties", stdin="4\na 7\nb 7\nc 2\nd 2\n"),
)


def _record_values(case: Case) -> list[int]:
    lines = case.stdin.splitlines()
    return [int(line.split()[1]) for line in lines[1:]]


RECORD_OPERATIONS = (
    (
        "first-max",
        "First Highest Lab Batch",
        lambda a: a.index(max(a)) if a else -1,
        "if(n==0)return -1;int at=0;for(int i=1;i<n;i++)if(a[i].value>a[at].value)at=i;return at;",
    ),
    (
        "positive",
        "Positive Wildlife Records",
        lambda a: sum(x > 0 for x in a),
        "long long x=0;for(int i=0;i<n;i++)if(a[i].value>0)x++;return x;",
    ),
    (
        "range",
        "Shipment Value Range",
        lambda a: max(a) - min(a) if a else 0,
        "if(n==0)return 0;int lo=a[0].value,hi=lo;for(int i=1;i<n;i++){if(a[i].value<lo)lo=a[i].value;if(a[i].value>hi)hi=a[i].value;}return (long long)hi-lo;",
    ),
    (
        "pairs",
        "Equal-Reading Record Pairs",
        lambda a: sum(a[i] == a[j] for i in range(len(a)) for j in range(i + 1, len(a))),
        "long long x=0;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(a[i].value==a[j].value)x++;return x;",
    ),
    (
        "run",
        "Longest Nondecreasing Record Run",
        lambda a: _longest(a, lambda x, y: y >= x),
        "if(n==0)return 0;int best=1,run=1;for(int i=1;i<n;i++){run=a[i].value>=a[i-1].value?run+1:1;if(run>best)best=run;}return best;",
    ),
)

RECORD_DEFINITIONS = {
    "first-max": "Return the zero-based index of the first maximum-valued record, or -1 when there are none.",
    "positive": "Count records whose value is strictly greater than zero.",
    "range": "Return maximum record value minus minimum record value, or 0 for no records.",
    "pairs": "Count record-index pairs `i < j` with equal values; names do not affect equality.",
    "run": "Return the longest contiguous nondecreasing run of record values, or 0 for no records.",
}


def _record_source(body: str, *, starter: bool) -> str:
    solve = (
        "static long long solve(const struct record*a,int n){(void)a;(void)n;return 0;}"
        if starter
        else f"static long long solve(const struct record*a,int n){{{body}}}"
    )
    return f'#include <stdio.h>\nstruct record{{char name[32];int value;}};\n{solve}\nint main(void){{int n;struct record a[50];if(scanf("%d",&n)!=1||n<0||n>50)return 1;for(int i=0;i<n;i++)if(scanf("%31s%d",a[i].name,&a[i].value)!=2)return 1;printf("result: %lld\\n",solve(a,n));return 0;}}\n'


def _record_questions() -> Iterable[AuthoredQuestion]:
    slots = ("short", "short", "short", "medium", "medium")
    difficulties = (2, 2, 3, 4, 4)
    for index, (key, title, op, body) in enumerate(RECORD_OPERATIONS, start=1):
        difficulty = difficulties[index - 1]

        def run(case: Case, operation: Callable[[list[int]], int] = op) -> tuple[str, str, int]:
            return f"result: {operation(_record_values(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1511-record-{index:03d}",
            title=title,
            course="COMP1511",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 3 else "normal",
            tags=("structs", "arrays-1d", "io", "loops", "functions"),
            weeks=(4, 5),
            slot=slots[index - 1],
            minutes=14 + difficulty * 4,
            background="Named records combine a short identifier with one signed measurement. The identifier establishes the input shape while the required result uses record order and values.",
            requirements="Read `n` (0 to 50), followed by `n` lines containing a whitespace-free name and signed value. Print `result: X`.",
            implementation_notes="Represent each item with a `struct`; use a width limit when scanning the 31-character name.",
            idea=f"Store each input row as one struct and compute {title.lower()} over the resulting record array.",
            steps=(
                "Read and validate the record count.",
                "Populate one complete struct per input row.",
                "Apply the metric without separating names from their values.",
                "Print the final scalar using the stated tie rule.",
            ),
            correctness="Every input row becomes exactly one array element in the same order. The helper's scan/pair enumeration matches the metric definition, so the final scalar is correct for all records.",
            complexity="Most variants run in `O(n)` time; the equal-pair variant uses `O(n^2)`. The record array uses `O(n)` space.",
            pitfalls="Limit `%s`, handle `n == 0`, and keep first-versus-last tie behaviour explicit.",
            starter=_record_source(body, starter=True),
            reference=_record_source(body, starter=False),
            cases=RECORD_CASES,
            oracle=run,
            definition=RECORD_DEFINITIONS[key],
        )


LEDGER_CASES = (
    Case("updates", stdin="ADD alpha 5\nADD beta -2\nSET beta 8\nTOTAL\nEND\n"),
    Case("empty", stdin="END\n"),
    Case("add-query", stdin="ADD alpha 5\nQUERY alpha\nEND\n"),
    Case("remove", stdin="ADD a 3\nADD b 4\nREMOVE a\nQUERY a\nTOTAL\nEND\n"),
    Case("repeated", stdin="ADD x 2\nADD x 5\nQUERY x\nSET y -1\nTOTAL\nEND\n"),
)


def _ledger_oracle(case: Case) -> tuple[str, str, int]:
    values: dict[str, int] = {}
    out = []
    for line in case.stdin.splitlines():
        parts = line.split()
        cmd = parts[0]
        if cmd == "END":
            break
        if cmd == "ADD":
            values[parts[1]] = values.get(parts[1], 0) + int(parts[2])
        elif cmd == "SET":
            values[parts[1]] = int(parts[2])
        elif cmd == "REMOVE":
            values.pop(parts[1], None)
        elif cmd == "QUERY":
            out.append(f"{parts[1]} {values.get(parts[1], 0)}")
        elif cmd == "TOTAL":
            out.append(f"TOTAL {sum(values.values())}")
    return ("\n".join(out) + ("\n" if out else ""), "", 0)


def _ledger_source(*, starter: bool) -> str:
    if starter:
        core = "/* TODO: implement the command loop and dynamic record table. */\n    (void)argc;(void)argv;return 0;"
    else:
        core = """(void)argc;(void)argv;struct record*a=NULL;int n=0,cap=0;char cmd[16],name[32];
    while(scanf("%15s",cmd)==1&&strcmp(cmd,"END")!=0){
        if(strcmp(cmd,"TOTAL")==0){long long total=0;for(int i=0;i<n;i++)total+=a[i].value;printf("TOTAL %lld\\n",total);continue;}
        if(scanf("%31s",name)!=1){free(a);return 1;}int at=-1;for(int i=0;i<n;i++)if(strcmp(a[i].name,name)==0)at=i;
        if(strcmp(cmd,"QUERY")==0){printf("%s %d\\n",name,at<0?0:a[at].value);continue;}
        if(strcmp(cmd,"REMOVE")==0){if(at>=0)a[at]=a[--n];continue;}
        int value;if(scanf("%d",&value)!=1){free(a);return 1;}if(at<0){if(n==cap){cap=cap?cap*2:4;void*p=realloc(a,(size_t)cap*sizeof*a);if(!p){free(a);return 1;}a=p;}at=n++;strcpy(a[at].name,name);a[at].value=0;}
        if(strcmp(cmd,"ADD")==0)a[at].value+=value;else if(strcmp(cmd,"SET")==0)a[at].value=value;else{free(a);return 1;}
    }free(a);return 0;"""
    return f"""#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct record{{char name[32];int value;}};
int main(int argc,char**argv){{{core}}}
"""


def _ledger_questions() -> Iterable[AuthoredQuestion]:
    scenarios = (
        ("Community Battery Ledger", "neighbourhood batteries"),
        ("Rescue Supply Register", "rescue supply bins"),
        ("Museum Crate Journal", "museum storage crates"),
        ("Wetland Sensor Registry", "wetland sensor stations"),
        ("Festival Token Console", "festival token accounts"),
        ("Orbital Sample Inventory", "orbital sample containers"),
    )
    for index, (title, setting) in enumerate(scenarios, start=1):
        difficulty = 4 if index <= 2 else 5
        yield AuthoredQuestion(
            id=f"c1511-system-{index:03d}",
            title=title,
            course="COMP1511",
            kind="c_program",
            difficulty=difficulty,
            track="challenge",
            tags=(
                "whole-program",
                "structs",
                "strings",
                "io",
                "conditionals",
                "dynamic-memory",
                "arrays-1d",
                "testing",
            ),
            weeks=(1, 2, 4, 5, 7),
            slot="whole_program",
            minutes=42 + difficulty * 4,
            background=f"An operator maintains {setting} through a line-oriented command console. Entries appear dynamically and must remain correct across updates and removals.",
            requirements="Process commands until `END`: `ADD name delta`, `SET name value`, `REMOVE name`, `QUERY name`, and `TOTAL`. Missing names have value zero. `QUERY` prints `name value`; `TOTAL` prints `TOTAL sum`. Other commands print nothing.",
            implementation_notes="Use a dynamic array of structs with bounded names. Growth must preserve existing records. Free the final allocation on every normal exit.",
            idea="Maintain one authoritative dynamic table and interpret each command as a small state transition.",
            steps=(
                "Read one command token and dispatch before reading command-specific fields.",
                "Search for the named record and create it only for `ADD` or `SET`.",
                "Apply the transition, growing the table safely when needed.",
                "Print only query results, then free the table after `END`.",
            ),
            correctness="Initially the table represents the empty mapping. Each command branch performs exactly the mapping update or observation in its definition, preserving the representation invariant that names are unique. By induction, every query and total reflects all preceding commands.",
            complexity="With `m` commands and at most `n` names, linear search gives `O(mn)` time and the dynamic table uses `O(n)` space.",
            pitfalls="Do not create entries for `QUERY`/`REMOVE`, lose the old pointer when `realloc` fails, print update acknowledgements, or forget that repeated `ADD` accumulates.",
            starter=_ledger_source(starter=True),
            reference=_ledger_source(starter=False),
            cases=LEDGER_CASES,
            oracle=_ledger_oracle,
            definition="The table maps unique names to signed values: `ADD` accumulates, `SET` replaces, `REMOVE` deletes, a missing `QUERY` returns zero, and `TOTAL` sums current values.",
        )


def comp1511_questions() -> tuple[AuthoredQuestion, ...]:
    questions = tuple(
        (
            *_sequence_questions(),
            *_list_questions(),
            *_string_questions(),
            *_numeric_questions(),
            *_grid_questions(),
            *_record_questions(),
            *_ledger_questions(),
        )
    )
    if len(questions) != 75:
        raise AssertionError(f"expected 75 COMP1511 questions, found {len(questions)}")
    return questions


# ---------------------------------------------------------------------------
# COMP1521 expansion catalogue


MASK32 = (1 << 32) - 1


BIT_CASES = (
    Case("patterns", stdin="12345678 00ff00ff 8\n"),
    Case("zero", stdin="00000000 00000000 0\n"),
    Case("high-bit", stdin="80000001 0f0f0f0f 31\n"),
    Case("all-bits", stdin="ffffffff aaaaaaaa 16\n"),
    Case("boundary", stdin="000000ff 0000ff00 4\n"),
)


def _bit_inputs(case: Case) -> tuple[int, int, int]:
    x, y, k = case.stdin.split()
    return int(x, 16), int(y, 16), int(k)


def _rotl(value: int, shift: int) -> int:
    shift &= 31
    return ((value << shift) | (value >> ((32 - shift) & 31))) & MASK32


def _rotr(value: int, shift: int) -> int:
    shift &= 31
    return ((value >> shift) | (value << ((32 - shift) & 31))) & MASK32


def _reverse_bits(value: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


def _sign_extend_8(value: int) -> int:
    value &= 0xFF
    return (value | 0xFFFFFF00) if value & 0x80 else value


def _binary32_class(value: int) -> int:
    exponent = (value >> 23) & 0xFF
    fraction = value & 0x7FFFFF
    if exponent == 0:
        return 1 if fraction else 0
    if exponent == 0xFF:
        return 4 if fraction else 3
    return 2


BIT_OPERATIONS: tuple[
    tuple[str, str, Callable[[int, int, int], int], str, tuple[str, ...]], ...
] = (
    (
        "low-byte",
        "Extract the Telemetry Low Byte",
        lambda x, y, k: x & 0xFF,
        "return x&0xffu;",
        ("bitwise", "integer-representation"),
    ),
    (
        "high-byte",
        "Extract the Packet High Byte",
        lambda x, y, k: (x >> 24) & 0xFF,
        "return (x>>24)&0xffu;",
        ("bitwise", "integer-representation"),
    ),
    (
        "xor",
        "Combine Redundant Sensor Masks",
        lambda x, y, k: x ^ y,
        "return x^y;",
        ("bitwise", "c-revision"),
    ),
    (
        "set",
        "Enable Permission Bits",
        lambda x, y, k: x | y,
        "return x|y;",
        ("bitwise", "integer-representation"),
    ),
    (
        "clear",
        "Clear Fault Mask Bits",
        lambda x, y, k: x & ~y & MASK32,
        "return x&~y;",
        ("bitwise", "integer-representation"),
    ),
    (
        "toggle",
        "Toggle Display Channels",
        lambda x, y, k: x ^ y,
        "return x^y;",
        ("bitwise", "c-revision"),
    ),
    (
        "rotl",
        "Rotate a Network Sequence Word",
        lambda x, y, k: _rotl(x, k),
        "k&=31u;return (x<<k)|(x>>((32u-k)&31u));",
        ("bitwise", "integer-representation"),
    ),
    (
        "rotr",
        "Rotate a Control Word Right",
        lambda x, y, k: _rotr(x, k),
        "k&=31u;return (x>>k)|(x<<((32u-k)&31u));",
        ("bitwise", "integer-representation"),
    ),
    (
        "popcount",
        "Count Active Relay Bits",
        lambda x, y, k: x.bit_count(),
        "uint32_t r=0;for(;x;x>>=1)r+=x&1u;return r;",
        ("bitwise", "integer-representation", "c-revision"),
    ),
    (
        "parity",
        "Compute Packet Bit Parity",
        lambda x, y, k: x.bit_count() & 1,
        "uint32_t r=0;for(;x;x>>=1)r^=x&1u;return r;",
        ("bitwise", "binary-data"),
    ),
    (
        "swap-nibbles",
        "Swap Byte Nibbles",
        lambda x, y, k: ((x & 0x0F0F0F0F) << 4 | (x & 0xF0F0F0F0) >> 4) & MASK32,
        "return ((x&0x0f0f0f0fu)<<4)|((x&0xf0f0f0f0u)>>4);",
        ("bitwise", "binary-data"),
    ),
    (
        "swap-halves",
        "Swap Register Halfwords",
        lambda x, y, k: ((x << 16) | (x >> 16)) & MASK32,
        "return (x<<16)|(x>>16);",
        ("bitwise", "integer-representation"),
    ),
    (
        "sign-extend",
        "Sign-Extend an Eight-Bit Reading",
        lambda x, y, k: _sign_extend_8(x),
        "uint32_t v=x&0xffu;return (v&0x80u)?v|0xffffff00u:v;",
        ("bitwise", "integer-representation", "c-revision"),
    ),
    (
        "field",
        "Extract a Five-Bit Register Field",
        lambda x, y, k: (x >> (k & 31)) & 0x1F,
        "return (x>>(k&31u))&0x1fu;",
        ("bitwise", "mips-basics", "integer-representation"),
    ),
    (
        "pack",
        "Pack Two Sixteen-Bit Counters",
        lambda x, y, k: ((x & 0xFFFF) << 16) | (y & 0xFFFF),
        "return ((x&0xffffu)<<16)|(y&0xffffu);",
        ("bitwise", "binary-data"),
    ),
    (
        "reverse",
        "Reverse a Diagnostic Bit String",
        lambda x, y, k: _reverse_bits(x),
        "uint32_t r=0;for(int i=0;i<32;i++){r=(r<<1)|(x&1u);x>>=1;}return r;",
        ("bitwise", "integer-representation"),
    ),
    (
        "masked-merge",
        "Merge Two Masked Device Words",
        lambda x, y, k: ((x & (MASK32 << (k & 31))) | (y & ~(MASK32 << (k & 31)))) & MASK32,
        "k&=31u;uint32_t mask=k?~0u<<k:~0u;return (x&mask)|(y&~mask);",
        ("bitwise", "binary-data"),
    ),
    (
        "binary32",
        "Classify a Binary32 Telemetry Word",
        lambda x, y, k: _binary32_class(x),
        "uint32_t e=(x>>23)&0xffu,f=x&0x7fffffu;if(e==0)return f?1u:0u;if(e==0xffu)return f?4u:3u;return 2u;",
        ("floating-point", "bitwise", "integer-representation"),
    ),
    (
        "mips-i",
        "Encode a Compact MIPS I-Format Word",
        lambda x, y, k: (
            (((x & 0x3F) << 26) | ((y & 0x1F) << 21) | ((k & 0x1F) << 16) | ((x ^ y) & 0xFFFF))
            & MASK32
        ),
        "return ((x&0x3fu)<<26)|((y&0x1fu)<<21)|((k&0x1fu)<<16)|((x^y)&0xffffu);",
        ("mips-basics", "bitwise", "integer-representation"),
    ),
    (
        "mips-r",
        "Decode a MIPS R-Format Register Checksum",
        lambda x, y, k: (
            (((x >> 21) & 31) + ((x >> 16) & 31) + ((x >> 11) & 31) + (x & 63)) & MASK32
        ),
        "return ((x>>21)&31u)+((x>>16)&31u)+((x>>11)&31u)+(x&63u);",
        ("mips-basics", "bitwise", "integer-representation"),
    ),
)

BIT_DEFINITIONS = {
    "low-byte": "Return bits 7 through 0 of `x`, equivalently `x & 0xFF`; ignore `y` and `k`.",
    "high-byte": "Return bits 31 through 24 of `x` as an unsigned value from 0 to 255; ignore `y` and `k`.",
    "xor": "Return the 32-bit bitwise exclusive OR `x ^ y`; ignore `k`.",
    "set": "Treat every 1 bit in `y` as a bit to enable and return `x | y`; ignore `k`.",
    "clear": "Treat every 1 bit in `y` as a bit to clear and return `x & ~y`; ignore `k`.",
    "toggle": "Treat every 1 bit in `y` as a bit to toggle and return `x ^ y`; ignore `k`.",
    "rotl": "Let `s = k % 32`; rotate `x` left by `s` bits, wrapping shifted-out bits into the low end.",
    "rotr": "Let `s = k % 32`; rotate `x` right by `s` bits, wrapping shifted-out bits into the high end.",
    "popcount": "Return the number of 1 bits in the 32-bit representation of `x`; ignore `y` and `k`.",
    "parity": "Return `popcount(x) % 2`: 0 for an even number of 1 bits and 1 for an odd number.",
    "swap-nibbles": "Within each of the four bytes of `x`, swap its high four bits with its low four bits.",
    "swap-halves": "Swap bits 31..16 with bits 15..0 of `x`; ignore `y` and `k`.",
    "sign-extend": "Take the low eight bits of `x` as an 8-bit two's-complement value and sign-extend it to a 32-bit pattern.",
    "field": "Let `s = k % 32`; return the low five bits of the logical right shift `x >> s`.",
    "pack": "Place the low 16 bits of `x` in result bits 31..16 and the low 16 bits of `y` in bits 15..0.",
    "reverse": "Return the 32-bit word whose bit `31 - i` equals bit `i` of `x` for every `i` from 0 to 31.",
    "masked-merge": "Let `s = k % 32`; take result bits `s..31` from `x` and bits `0..s-1` from `y` (so `s == 0` returns `x`).",
    "binary32": "Interpret only the IEEE-754 binary32 exponent and fraction fields of `x`: return 0 for zero, 1 for subnormal, 2 for finite normal, 3 for infinity, and 4 for NaN.",
    "mips-i": "Encode opcode=`x & 63`, rs=`y & 31`, rt=`k & 31`, and immediate=`(x ^ y) & 65535` into the standard MIPS I-format bit positions.",
    "mips-r": "From `x`, extract rs (bits 25..21), rt (20..16), rd (15..11), and funct (5..0), then return their unsigned sum.",
}


def _bit_source(body: str, *, starter: bool) -> str:
    solve = (
        "static uint32_t solve(uint32_t x,uint32_t y,unsigned k){(void)x;(void)y;(void)k;return 0;}"
        if starter
        else f"static uint32_t solve(uint32_t x,uint32_t y,unsigned k){{(void)x;(void)y;(void)k;{body}}}"
    )
    return f"""#include <stdint.h>
#include <stdio.h>
{solve}
int main(void){{unsigned x,y,k;if(scanf("%x%x%u",&x,&y,&k)!=3)return 1;printf("result: %08x\\n",solve(x,y,k));return 0;}}
"""


def _bit_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4)
    for index, (key, title, operation, body, tags) in enumerate(BIT_OPERATIONS, start=1):
        slot = "foundation" if index <= 15 else "advanced_systems"
        difficulty = difficulties[index - 1]

        def run(case: Case, op: Callable[[int, int, int], int] = operation) -> tuple[str, str, int]:
            return f"result: {op(*_bit_inputs(case)) & MASK32:08x}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1521-bits-{index:03d}",
            title=title,
            course="COMP1521",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 4 else "normal",
            tags=tags,
            weeks=(2, 3, 4),
            slot=slot,
            minutes=12 + difficulty * 4,
            background="A systems utility represents compact state in one 32-bit word. The transformation must be explicit about unsigned shifts, masks, and field widths.",
            requirements="Read two hexadecimal 32-bit words `x y` and a decimal shift or field value `k`. Print the computed value as `result: XXXXXXXX` using exactly eight lowercase hexadecimal digits.",
            implementation_notes="Use `uint32_t`. Reduce variable shifts to 0 through 31 before shifting, and never shift a 32-bit value by 32.",
            idea=f"Use masks and unsigned shifts to implement {title.lower()} without string conversion.",
            steps=(
                "Parse the two words as unsigned hexadecimal values.",
                "Construct each mask from the documented field width.",
                "Shift only unsigned values and combine disjoint fields with bitwise operators.",
                "Print the final 32-bit pattern with fixed width.",
            ),
            correctness="Each mask retains exactly the bits belonging to its named field, and each shift moves those bits to the required positions. The final OR/XOR therefore contains exactly the specified result bits.",
            complexity="A fixed number of word operations uses `O(1)` time and space; bit-count/reversal variants use exactly 32 iterations.",
            pitfalls="Signed right shift, a shift count of 32, a missing `u` suffix, or printing decimal instead of eight-digit hexadecimal changes observable behaviour.",
            starter=_bit_source(body, starter=True),
            reference=_bit_source(body, starter=False),
            cases=BIT_CASES,
            oracle=run,
            definition=BIT_DEFINITIONS[key],
        )


MIPS_CASES = SEQUENCE_CASES


def _mips_operation_values(case: Case) -> list[int]:
    return _values(case)


MIPS_OPERATIONS: tuple[tuple[str, str, Callable[[list[int]], int], str], ...] = (
    (
        "sum",
        "MIPS Stream Total",
        sum,
        "move $t0,$a0\nmove $t1,$a1\nli $v0,0\nms1: beq $t1,$zero,ms9\nlw $t2,0($t0)\naddu $v0,$v0,$t2\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb ms1\nms9: jr $ra",
    ),
    (
        "positive",
        "MIPS Positive Reading Count",
        lambda a: sum(x > 0 for x in a),
        "move $t0,$a0\nmove $t1,$a1\nli $v0,0\nmp1: beq $t1,$zero,mp9\nlw $t2,0($t0)\nslt $t3,$zero,$t2\naddu $v0,$v0,$t3\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mp1\nmp9: jr $ra",
    ),
    (
        "even",
        "MIPS Even Sample Count",
        lambda a: sum(x % 2 == 0 for x in a),
        "move $t0,$a0\nmove $t1,$a1\nli $v0,0\nme1: beq $t1,$zero,me9\nlw $t2,0($t0)\nandi $t3,$t2,1\nbne $t3,$zero,me2\naddiu $v0,$v0,1\nme2: addiu $t0,$t0,4\naddiu $t1,$t1,-1\nb me1\nme9: jr $ra",
    ),
    (
        "nonzero",
        "MIPS Nonzero Channel Count",
        lambda a: sum(x != 0 for x in a),
        "move $t0,$a0\nmove $t1,$a1\nli $v0,0\nmn1: beq $t1,$zero,mn9\nlw $t2,0($t0)\nbeq $t2,$zero,mn2\naddiu $v0,$v0,1\nmn2: addiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mn1\nmn9: jr $ra",
    ),
    (
        "max",
        "MIPS Maximum Buffer Value",
        lambda a: max(a, default=0),
        "beq $a1,$zero,mm0\nlw $v0,0($a0)\naddiu $t0,$a0,4\naddiu $t1,$a1,-1\nmm1: beq $t1,$zero,mm9\nlw $t2,0($t0)\nslt $t3,$v0,$t2\nbeq $t3,$zero,mm2\nmove $v0,$t2\nmm2: addiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mm1\nmm0: li $v0,0\nmm9: jr $ra",
    ),
    (
        "min",
        "MIPS Minimum Buffer Value",
        lambda a: min(a, default=0),
        "beq $a1,$zero,mi0\nlw $v0,0($a0)\naddiu $t0,$a0,4\naddiu $t1,$a1,-1\nmi1: beq $t1,$zero,mi9\nlw $t2,0($t0)\nslt $t3,$t2,$v0\nbeq $t3,$zero,mi2\nmove $v0,$t2\nmi2: addiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mi1\nmi0: li $v0,0\nmi9: jr $ra",
    ),
    (
        "alternating",
        "MIPS Alternating Register Total",
        lambda a: sum(x if i % 2 == 0 else -x for i, x in enumerate(a)),
        "move $t0,$a0\nmove $t1,$a1\nli $t2,0\nli $v0,0\nma1: beq $t1,$zero,ma9\nlw $t3,0($t0)\nandi $t4,$t2,1\nbeq $t4,$zero,ma2\nsubu $v0,$v0,$t3\nb ma3\nma2: addu $v0,$v0,$t3\nma3: addiu $t2,$t2,1\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb ma1\nma9: jr $ra",
    ),
    (
        "xor",
        "MIPS XOR Buffer Fold",
        lambda a: _xor_values(a),
        "move $t0,$a0\nmove $t1,$a1\nli $v0,0\nmx1: beq $t1,$zero,mx9\nlw $t2,0($t0)\nxor $v0,$v0,$t2\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mx1\nmx9: jr $ra",
    ),
    (
        "rises",
        "MIPS Adjacent Rise Count",
        lambda a: sum(y > x for x, y in zip(a, a[1:], strict=False)),
        "slti $t7,$a1,2\nbne $t7,$zero,mr0\nlw $t2,0($a0)\naddiu $t0,$a0,4\naddiu $t1,$a1,-1\nli $v0,0\nmr1: beq $t1,$zero,mr9\nlw $t3,0($t0)\nslt $t4,$t2,$t3\naddu $v0,$v0,$t4\nmove $t2,$t3\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mr1\nmr0: li $v0,0\nmr9: jr $ra",
    ),
    (
        "weighted",
        "MIPS Position-Weighted Checksum",
        lambda a: sum((i + 1) * x for i, x in enumerate(a)),
        "move $t0,$a0\nmove $t1,$a1\nli $t2,1\nli $v0,0\nmw1: beq $t1,$zero,mw9\nlw $t3,0($t0)\nmult $t2,$t3\nmflo $t4\naddu $v0,$v0,$t4\naddiu $t2,$t2,1\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mw1\nmw9: jr $ra",
    ),
    (
        "first-max",
        "MIPS First Maximum Index Function",
        lambda a: a.index(max(a)) if a else -1,
        "beq $a1,$zero,mf0\nlw $t4,0($a0)\nli $v0,0\nli $t2,1\naddiu $t0,$a0,4\nmf1: beq $t2,$a1,mf9\nlw $t3,0($t0)\nslt $t5,$t4,$t3\nbeq $t5,$zero,mf2\nmove $t4,$t3\nmove $v0,$t2\nmf2: addiu $t2,$t2,1\naddiu $t0,$t0,4\nb mf1\nmf0: li $v0,-1\nmf9: jr $ra",
    ),
    (
        "range",
        "MIPS Buffer Range Function",
        lambda a: max(a) - min(a) if a else 0,
        "beq $a1,$zero,mg0\nlw $t4,0($a0)\nmove $t5,$t4\naddiu $t0,$a0,4\naddiu $t1,$a1,-1\nmg1: beq $t1,$zero,mg8\nlw $t3,0($t0)\nslt $t6,$t3,$t4\nbeq $t6,$zero,mg2\nmove $t4,$t3\nmg2: slt $t6,$t5,$t3\nbeq $t6,$zero,mg3\nmove $t5,$t3\nmg3: addiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mg1\nmg8: subu $v0,$t5,$t4\njr $ra\nmg0: li $v0,0\njr $ra",
    ),
    (
        "absolute",
        "MIPS Absolute Buffer Total",
        lambda a: sum(abs(x) for x in a),
        "move $t0,$a0\nmove $t1,$a1\nli $v0,0\nmb1: beq $t1,$zero,mb9\nlw $t2,0($t0)\nbgez $t2,mb2\nsubu $t2,$zero,$t2\nmb2: addu $v0,$v0,$t2\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mb1\nmb9: jr $ra",
    ),
    (
        "equal-pairs",
        "MIPS Equal Neighbour Count",
        lambda a: sum(x == y for x, y in zip(a, a[1:], strict=False)),
        "slti $t7,$a1,2\nbne $t7,$zero,mq0\nlw $t2,0($a0)\naddiu $t0,$a0,4\naddiu $t1,$a1,-1\nli $v0,0\nmq1: beq $t1,$zero,mq9\nlw $t3,0($t0)\nbne $t2,$t3,mq2\naddiu $v0,$v0,1\nmq2: move $t2,$t3\naddiu $t0,$t0,4\naddiu $t1,$t1,-1\nb mq1\nmq0: li $v0,0\nmq9: jr $ra",
    ),
    (
        "last",
        "MIPS Last Buffer Reading",
        lambda a: a[-1] if a else 0,
        "beq $a1,$zero,ml0\naddiu $t1,$a1,-1\nsll $t1,$t1,2\naddu $t0,$a0,$t1\nlw $v0,0($t0)\njr $ra\nml0: li $v0,0\njr $ra",
    ),
)

MIPS_DEFINITIONS = {
    "sum": "Return the sum of all array elements, or 0 for an empty array.",
    "positive": "Count elements strictly greater than zero; zero does not count.",
    "even": "Count elements divisible by two, including zero and negative even values.",
    "nonzero": "Count elements that are not equal to zero.",
    "max": "Return the greatest element, or 0 for an empty array.",
    "min": "Return the smallest element, or 0 for an empty array.",
    "alternating": "Compute `a[0] - a[1] + a[2] - a[3] + ...`, or 0 for an empty array.",
    "xor": "Bitwise-XOR all 32-bit element patterns from left to right, starting from zero.",
    "rises": "Count adjacent pairs `(a[i-1], a[i])` for which the later value is strictly greater.",
    "weighted": "Compute `sum((i + 1) * a[i])` with one-based position weights.",
    "first-max": "Return the zero-based index of the first greatest element, or -1 for an empty array.",
    "range": "Return `maximum - minimum`, or 0 for an empty array.",
    "absolute": "Return the sum of the absolute values of all elements.",
    "equal-pairs": "Count adjacent pairs whose values are equal; overlapping pairs count separately.",
    "last": "Return the final array element, or 0 for an empty array.",
}


def _xor_values(values: Sequence[int]) -> int:
    result = 0
    for value in values:
        result ^= value & MASK32
    return result - (1 << 32) if result & (1 << 31) else result


def _mips_source(body: str, *, starter: bool) -> str:
    solve = "solve:\n    li $v0,0\n    jr $ra" if starter else f"solve:\n{_indent_asm(body)}"
    return f""".data
values: .space 400
.text
.globl main
main:
    li $v0,5
    syscall
    move $s0,$v0
    la $s1,values
    li $t0,0
read_loop:
    beq $t0,$s0,read_done
    li $v0,5
    syscall
    sll $t1,$t0,2
    addu $t2,$s1,$t1
    sw $v0,0($t2)
    addiu $t0,$t0,1
    b read_loop
read_done:
    move $a0,$s1
    move $a1,$s0
    jal solve
    move $a0,$v0
    li $v0,1
    syscall
    li $a0,10
    li $v0,11
    syscall
    li $v0,10
    syscall
{solve}
"""


def _indent_asm(source: str) -> str:
    return "\n".join(line if line.endswith(":") else f"    {line}" for line in source.splitlines())


def _mips_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4)
    for index, (key, title, operation, body) in enumerate(MIPS_OPERATIONS, start=1):
        slot = "foundation" if index <= 10 else "advanced_systems"
        difficulty = difficulties[index - 1]

        def run(case: Case, op: Callable[[list[int]], int] = operation) -> tuple[str, str, int]:
            return f"{op(_mips_operation_values(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1521-mips-{index:03d}",
            title=title,
            course="COMP1521",
            kind="mips_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 4 else "normal",
            tags=(
                "mips-basics",
                "mips-control",
                "mips-data",
                "mips-functions",
                "integer-representation",
            ),
            weeks=(1, 2, 3, 4),
            slot=slot,
            minutes=14 + difficulty * 5,
            background="A MIPS32 routine receives a pointer and element count after `main` reads a bounded integer stream. The routine must obey the register interface and return one scalar in `$v0`.",
            requirements="Read `n` (0 to 100) and `n` signed integers. `main` calls `solve($a0 = array, $a1 = n)`. Implement `solve`, return the computed value in `$v0`, and let `main` print it with one newline.",
            implementation_notes="Use word-aligned loads, advance pointers by four bytes, and do not issue input/output syscalls inside `solve`.",
            idea=f"Translate the loop invariant for {title.lower()} into a leaf MIPS function.",
            steps=(
                "Handle the zero-length base case before loading element zero.",
                "Copy pointer/count arguments into temporary registers.",
                "Update the accumulator and pointer once per element.",
                "Return through `$ra` with the final value in `$v0`.",
            ),
            correctness="At each loop header, the accumulator equals the required metric for the already-consumed prefix and the pointer names the next word. One iteration adds exactly that word's contribution, so termination after `n` words returns the full metric.",
            complexity="The routine uses `O(n)` instructions and `O(1)` extra storage.",
            pitfalls="Do not overwrite `$ra`, confuse byte and word offsets, load before checking `n == 0`, or leave the result in a temporary register.",
            starter=_mips_source(body, starter=True),
            reference=_mips_source(body, starter=False),
            cases=MIPS_CASES,
            oracle=run,
            extension=".s",
            definition=MIPS_DEFINITIONS[key],
        )


FILE_CASES = (
    Case("ascii", args=("input.bin",), fixtures=(("ascii.bin", "input.bin", b"A1b2C3\n"),)),
    Case("empty", args=("input.bin",), fixtures=(("empty.bin", "input.bin", b""),)),
    Case(
        "binary",
        args=("input.bin",),
        fixtures=(("binary.bin", "input.bin", bytes((0, 255, 1, 128, 0, 2))),),
    ),
    Case("lines", args=("input.bin",), fixtures=(("lines.bin", "input.bin", b"one\ntwo\n\n"),)),
    Case("runs", args=("input.bin",), fixtures=(("runs.bin", "input.bin", b"aaabccccc"),)),
)


def _fixture_bytes(case: Case) -> bytes:
    return case.fixtures[0][2]


def _byte_transitions(data: bytes) -> int:
    return sum(a != b for a, b in zip(data, data[1:], strict=False))


def _longest_byte_run(data: bytes) -> int:
    return _longest(data, lambda a, b: a == b)


FILE_OPERATIONS: tuple[tuple[str, str, Callable[[bytes], int], str], ...] = (
    ("size", "POSIX Byte Count", len, "return (long long)n;"),
    (
        "newlines",
        "POSIX Newline Count",
        lambda d: d.count(10),
        "long long r=0;for(size_t i=0;i<n;i++)if(a[i]=='\\n')r++;return r;",
    ),
    (
        "zeros",
        "Binary Zero Byte Count",
        lambda d: d.count(0),
        "long long r=0;for(size_t i=0;i<n;i++)if(a[i]==0)r++;return r;",
    ),
    (
        "digits",
        "ASCII Digit Byte Count",
        lambda d: sum(48 <= x <= 57 for x in d),
        "long long r=0;for(size_t i=0;i<n;i++)if(a[i]>='0'&&a[i]<='9')r++;return r;",
    ),
    (
        "sum",
        "Byte Sum Modulo 65536",
        lambda d: sum(d) & 0xFFFF,
        "long long r=0;for(size_t i=0;i<n;i++)r=(r+a[i])&0xffff;return r;",
    ),
    (
        "xor",
        "Binary XOR Fingerprint",
        lambda d: _xor_bytes(d),
        "unsigned r=0;for(size_t i=0;i<n;i++)r^=a[i];return r;",
    ),
    (
        "printable",
        "Printable ASCII Byte Count",
        lambda d: sum(32 <= x <= 126 for x in d),
        "long long r=0;for(size_t i=0;i<n;i++)if(a[i]>=32&&a[i]<=126)r++;return r;",
    ),
    (
        "high",
        "High-Bit Byte Count",
        lambda d: sum(x >= 128 for x in d),
        "long long r=0;for(size_t i=0;i<n;i++)if(a[i]&0x80)r++;return r;",
    ),
    (
        "transitions",
        "Adjacent Byte Transition Count",
        _byte_transitions,
        "long long r=0;for(size_t i=1;i<n;i++)if(a[i]!=a[i-1])r++;return r;",
    ),
    (
        "run",
        "Longest Identical Byte Run",
        _longest_byte_run,
        "if(n==0)return 0;long long best=1,run=1;for(size_t i=1;i<n;i++){run=a[i]==a[i-1]?run+1:1;if(run>best)best=run;}return best;",
    ),
    (
        "first-zero",
        "First Zero Byte Offset",
        lambda d: d.find(b"\0"),
        "for(size_t i=0;i<n;i++)if(a[i]==0)return (long long)i;return -1;",
    ),
    (
        "last-newline",
        "Last Newline Offset",
        lambda d: d.rfind(b"\n"),
        "long long at=-1;for(size_t i=0;i<n;i++)if(a[i]=='\\n')at=(long long)i;return at;",
    ),
    (
        "even",
        "Even Byte Count",
        lambda d: sum(x % 2 == 0 for x in d),
        "long long r=0;for(size_t i=0;i<n;i++)if((a[i]&1)==0)r++;return r;",
    ),
    ("records", "Complete Four-Byte Records", lambda d: len(d) // 4, "return (long long)(n/4);"),
    (
        "weighted",
        "Position-Weighted Byte Checksum",
        lambda d: sum((i + 1) * x for i, x in enumerate(d)) & 0x7FFFFFFF,
        "long long r=0;for(size_t i=0;i<n;i++)r=(r+(long long)(i+1)*a[i])&0x7fffffff;return r;",
    ),
)

FILE_DEFINITIONS = {
    "size": "Return the exact number of bytes in the file; an empty file has size 0.",
    "newlines": "Count bytes equal to hexadecimal `0A` (ASCII newline).",
    "zeros": "Count bytes equal to hexadecimal `00`; embedded zero bytes are ordinary data.",
    "digits": "Count bytes from `0x30` through `0x39` inclusive (ASCII `0` through `9`).",
    "sum": "Add every unsigned byte value and return the sum modulo 65536.",
    "xor": "Bitwise-XOR every unsigned byte value, starting from zero.",
    "printable": "Count bytes in the inclusive printable-ASCII range `0x20` through `0x7E`.",
    "high": "Count bytes whose most significant bit is 1, equivalently values from 128 through 255.",
    "transitions": "Count adjacent byte pairs whose values differ; a file shorter than two bytes returns 0.",
    "run": "Return the longest contiguous run of identical bytes, or 0 for an empty file.",
    "first-zero": "Return the zero-based offset of the first `0x00` byte, or -1 if none exists.",
    "last-newline": "Return the zero-based offset of the last `0x0A` byte, or -1 if none exists.",
    "even": "Count unsigned byte values divisible by two, including `0x00`.",
    "records": "Return the number of complete non-overlapping four-byte records, which is `file_size / 4` using integer division.",
    "weighted": "Return `sum((i + 1) * byte[i]) modulo 2^31`, using unsigned bytes and one-based offsets.",
}


def _xor_bytes(data: bytes) -> int:
    result = 0
    for value in data:
        result ^= value
    return result


def _file_source(body: str, *, starter: bool) -> str:
    solve = (
        "static long long solve(const unsigned char*a,size_t n){(void)a;(void)n;return 0;}"
        if starter
        else f"static long long solve(const unsigned char*a,size_t n){{(void)a;(void)n;{body}}}"
    )
    return f"""#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
{solve}
int main(int argc,char**argv){{if(argc!=2)return 1;int fd=open(argv[1],O_RDONLY);if(fd<0)return 1;size_t n=0,cap=256;unsigned char*a=malloc(cap);if(!a){{close(fd);return 1;}}for(;;){{if(n==cap){{cap*=2;void*p=realloc(a,cap);if(!p){{free(a);close(fd);return 1;}}a=p;}}ssize_t got=read(fd,a+n,cap-n);if(got<0){{free(a);close(fd);return 1;}}if(got==0)break;n+=(size_t)got;}}close(fd);printf("result: %lld\\n",solve(a,n));free(a);return 0;}}
"""


def _file_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4)
    for index, (key, title, op, body) in enumerate(FILE_OPERATIONS, start=1):
        slot = "foundation" if index <= 8 else "advanced_systems"
        difficulty = difficulties[index - 1]

        def run(case: Case, operation: Callable[[bytes], int] = op) -> tuple[str, str, int]:
            return f"result: {operation(_fixture_bytes(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1521-file-{index:03d}",
            title=title,
            course="COMP1521",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 4 else "normal",
            tags=("file-io", "binary-data", "c-revision"),
            weeks=(7, 8),
            slot=slot,
            minutes=14 + difficulty * 5,
            background="A binary-safe command-line utility must inspect a regular file without assuming text encoding or a terminating zero byte.",
            requirements="The program accepts exactly one file path. The supplied code reads its complete byte stream and passes the bytes to `solve`. Print the computed value as `result: X` followed by one newline. Empty files are valid.",
            implementation_notes="Treat the input as binary data: use `n`, not `strlen`, and compare each byte as an `unsigned char`. Do not change the supplied file-reading and cleanup code.",
            idea=f"Read the file as bytes and scan once to compute {title.lower()}.",
            steps=(
                "Validate the argument and open the file read-only.",
                "Read until EOF, handling short reads and capacity growth.",
                "Apply the byte-level invariant without string functions.",
                "Close, print, and free all owned storage.",
            ),
            correctness="The read loop appends every byte exactly once and stops only at EOF. The helper processes exactly that byte array, so its accumulator equals the defined file metric.",
            complexity="Reading and scanning use `O(n)` time and the byte buffer uses `O(n)` space.",
            pitfalls="Do not use `strlen`, treat byte 255 as EOF, assume one `read` fills the buffer, or leak the descriptor after an allocation error.",
            starter=_file_source(body, starter=True),
            reference=_file_source(body, starter=False),
            cases=FILE_CASES,
            oracle=run,
            definition=FILE_DEFINITIONS[key],
        )


UNICODE_CASES = (
    Case("three-byte", stdin="000020ac\n"),
    Case("ascii", stdin="00000041\n"),
    Case("two-byte", stdin="000000e9\n"),
    Case("four-byte", stdin="0001f642\n"),
    Case("invalid", stdin="0000d800\n"),
)


def _codepoint(case: Case) -> int:
    return int(case.stdin, 16)


def _scalar(cp: int) -> bool:
    return 0 <= cp <= 0x10FFFF and not 0xD800 <= cp <= 0xDFFF


def _utf8(cp: int) -> bytes:
    if not _scalar(cp):
        return b""
    return chr(cp).encode()


UNICODE_OPERATIONS = (
    (
        "valid",
        "Unicode Scalar Validity",
        lambda cp: int(_scalar(cp)),
        "return cp<=0x10ffffu&&!(cp>=0xd800u&&cp<=0xdfffu);",
    ),
    (
        "width",
        "UTF-8 Encoded Width",
        lambda cp: len(_utf8(cp)) if _scalar(cp) else -1,
        "if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;if(cp<=0x7fu)return 1;if(cp<=0x7ffu)return 2;if(cp<=0xffffu)return 3;return 4;",
    ),
    (
        "continuations",
        "UTF-8 Continuation Byte Count",
        lambda cp: max(0, len(_utf8(cp)) - 1) if _scalar(cp) else -1,
        "long long w;if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;if(cp<=0x7fu)w=1;else if(cp<=0x7ffu)w=2;else if(cp<=0xffffu)w=3;else w=4;return w-1;",
    ),
    (
        "first",
        "UTF-8 Leading Byte",
        lambda cp: _utf8(cp)[0] if _scalar(cp) else -1,
        "if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;if(cp<=0x7fu)return cp;if(cp<=0x7ffu)return 0xc0u|(cp>>6);if(cp<=0xffffu)return 0xe0u|(cp>>12);return 0xf0u|(cp>>18);",
    ),
    (
        "sum",
        "UTF-8 Byte Checksum",
        lambda cp: sum(_utf8(cp)) if _scalar(cp) else -1,
        "if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;if(cp<=0x7fu)return cp;if(cp<=0x7ffu)return (0xc0u|(cp>>6))+(0x80u|(cp&63u));if(cp<=0xffffu)return (0xe0u|(cp>>12))+(0x80u|((cp>>6)&63u))+(0x80u|(cp&63u));return (0xf0u|(cp>>18))+(0x80u|((cp>>12)&63u))+(0x80u|((cp>>6)&63u))+(0x80u|(cp&63u));",
    ),
    (
        "utf16",
        "UTF-16 Code Unit Count",
        lambda cp: 1 if _scalar(cp) and cp <= 0xFFFF else 2 if _scalar(cp) else -1,
        "if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;return cp<=0xffffu?1:2;",
    ),
    (
        "plane",
        "Unicode Plane Number",
        lambda cp: cp >> 16 if _scalar(cp) else -1,
        "if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;return cp>>16;",
    ),
    (
        "boundary",
        "UTF-8 Boundary Class",
        lambda cp: (
            0
            if not _scalar(cp)
            else 1
            if cp <= 0x7F
            else 2
            if cp <= 0x7FF
            else 3
            if cp <= 0xFFFF
            else 4
        ),
        "if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return 0;if(cp<=0x7fu)return 1;if(cp<=0x7ffu)return 2;if(cp<=0xffffu)return 3;return 4;",
    ),
)

UNICODE_DEFINITIONS = {
    "valid": "Return 1 exactly when `cp <= 0x10FFFF` and `cp` is not in the surrogate range `0xD800..0xDFFF`; otherwise return 0.",
    "width": "Return the canonical UTF-8 width: 1 for `0..0x7F`, 2 for `0x80..0x7FF`, 3 for `0x800..0xFFFF`, and 4 above that; return -1 for a non-scalar.",
    "continuations": "Return the canonical UTF-8 width minus one, or -1 for a non-scalar.",
    "first": "Return the unsigned value of the first byte in the canonical UTF-8 encoding, or -1 for a non-scalar.",
    "sum": "Add the unsigned byte values in the canonical UTF-8 encoding; return -1 for a non-scalar.",
    "utf16": "Return 1 UTF-16 code unit for a scalar at or below `0xFFFF`, 2 units above it, and -1 for a non-scalar.",
    "plane": "Return `cp >> 16` for a Unicode scalar (planes 0 through 16), or -1 for a non-scalar.",
    "boundary": "Return 0 for a non-scalar; otherwise return 1, 2, 3, or 4 according to the scalar's canonical UTF-8 width.",
}


def _unicode_source(body: str, *, starter: bool) -> str:
    solve = (
        "static long long solve(uint32_t cp){(void)cp;return 0;}"
        if starter
        else f"static long long solve(uint32_t cp){{{body}}}"
    )
    return f'#include <stdint.h>\n#include <stdio.h>\n{solve}\nint main(void){{unsigned cp;if(scanf("%x",&cp)!=1)return 1;printf("result: %lld\\n",solve(cp));return 0;}}\n'


def _unicode_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (2, 2, 3, 3, 3, 3, 4, 4)
    for index, (key, title, op, body) in enumerate(UNICODE_OPERATIONS, start=1):
        difficulty = difficulties[index - 1]

        def run(case: Case, operation: Callable[[int], int] = op) -> tuple[str, str, int]:
            return f"result: {operation(_codepoint(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1521-unicode-{index:03d}",
            title=title,
            course="COMP1521",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 4 else "normal",
            tags=("unicode", "bitwise", "integer-representation"),
            weeks=(5, 6),
            slot="unicode",
            minutes=14 + difficulty * 5,
            background="A Unicode boundary utility receives one numeric code point and must reason about scalar validity and variable-width encodings without depending on locale.",
            requirements="Read one hexadecimal code point and print the computed value as `result: X` followed by one newline. Surrogates and values above U+10FFFF are invalid and use the task rule's stated invalid result.",
            implementation_notes="Derive UTF-8 fields with masks and shifts. Validate scalar range before encoding.",
            idea=f"Classify the scalar range first, then derive {title.lower()} from the UTF-8/UTF-16 boundary table.",
            steps=(
                "Reject non-scalars, including the surrogate interval.",
                "Select the encoding width from inclusive boundary values.",
                "Build any requested leading/continuation fields with masks.",
                "Return the exact integer result.",
            ),
            correctness="The scalar ranges are disjoint and cover every valid code point. Each branch applies the encoding formula for that range, so the returned width/byte/classification is exact.",
            complexity="A constant number of comparisons and shifts uses `O(1)` time and space.",
            pitfalls="Do not accept surrogates, use `<` where an inclusive boundary needs `<=`, or confuse a code point with an already encoded byte.",
            starter=_unicode_source(body, starter=True),
            reference=_unicode_source(body, starter=False),
            cases=UNICODE_CASES,
            oracle=run,
            definition=UNICODE_DEFINITIONS[key],
        )


TREE_CASES = (
    Case(
        "nested",
        args=("tree",),
        fixtures=(("one.c", "tree/src/one.c", b"int x;\n"), ("two.bin", "tree/build/two.o", b"1234")),
    ),
    Case("empty-tree", args=("tree",), fixtures=(("keep-empty.bin", "tree/.keep", b""),)),
    Case(
        "flat",
        args=("tree",),
        fixtures=(("a.txt", "tree/a.txt", b"abc"), ("b.bin", "tree/b.bin", b"12")),
    ),
    Case("deep", args=("tree",), fixtures=(("deep.txt", "tree/a/b/c/deep.txt", b"hello"),)),
    Case(
        "mixed",
        args=("tree",),
        fixtures=(
            ("x.c", "tree/x.c", b"x"),
            ("y.txt", "tree/sub/y.txt", b"yy"),
            ("z.bin", "tree/sub/z.bin", b"zzz"),
        ),
    ),
)


def _tree_files(case: Case) -> list[tuple[str, bytes]]:
    return [
        (target.removeprefix("tree/"), content)
        for _, target, content in case.fixtures
        if not target.endswith(".keep")
    ]


def _tree_dirs(case: Case) -> set[str]:
    dirs = {"."}
    for path, _ in _tree_files(case):
        parts = Path(path).parts
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]))
    return dirs


TREE_OPERATIONS = (
    (
        "files",
        "Recursive Regular File Count",
        lambda c: len(_tree_files(c)),
        "s.files",
        ("directories", "recursive-traversal", "file-metadata"),
        0,
    ),
    (
        "bytes",
        "Recursive Tree Byte Total",
        lambda c: sum(len(x) for _, x in _tree_files(c)),
        "s.bytes",
        ("directories", "recursive-traversal", "file-metadata"),
        1,
    ),
    (
        "depth",
        "Maximum File Tree Depth",
        lambda c: max((len(Path(p).parts) - 1 for p, _ in _tree_files(c)), default=0),
        "s.depth",
        ("directories", "recursive-traversal", "file-metadata"),
        2,
    ),
    (
        "text",
        "Recursive Text File Count",
        lambda c: sum(p.endswith(".txt") for p, _ in _tree_files(c)),
        "s.text",
        ("directories", "recursive-traversal", "file-io"),
        3,
    ),
    (
        "dirs",
        "Recursive Directory Count",
        lambda c: len(_tree_dirs(c)),
        "s.dirs",
        ("directories", "recursive-traversal", "file-metadata"),
        4,
    ),
    (
        "largest",
        "Largest Recursive File Size",
        lambda c: max((len(x) for _, x in _tree_files(c)), default=0),
        "s.largest",
        ("directories", "recursive-traversal", "file-metadata"),
        5,
    ),
    (
        "sources",
        "Recursive Build Source Count",
        lambda c: sum(p.endswith(".c") for p, _ in _tree_files(c)),
        "s.sources",
        ("directories", "recursive-traversal", "file-metadata", "make"),
        6,
    ),
)

TREE_DEFINITIONS = {
    "files": "Count regular files anywhere below the supplied root. Directories and the reserved `.keep` placeholder do not count.",
    "bytes": "Sum `st_size` for every real regular file below the root; an empty tree returns 0.",
    "depth": "The root has depth 0 and a file's depth is the number of containing subdirectories below the root; return the maximum file depth, or 0 if there are no files.",
    "text": "Count real regular files whose basename ends exactly with the case-sensitive suffix `.txt`.",
    "dirs": "Count the supplied root and every real directory recursively below it; regular files do not count.",
    "largest": "Return the greatest `st_size` among real regular files, or 0 when the tree contains none.",
    "sources": "Count real regular files whose basename ends exactly with the case-sensitive suffix `.c`.",
}


def _tree_source(result_body: str, *, starter: bool) -> str:
    if starter:
        walk = "static int walk(const char*path,int depth,struct summary*s){(void)path;(void)depth;(void)s;return -1;}"
    else:
        walk = """static int walk(const char*path,int depth,struct summary*s){DIR*d=opendir(path);if(!d)return -1;s->dirs++;struct dirent*e;while((e=readdir(d))){if(strcmp(e->d_name,".")==0||strcmp(e->d_name,"..")==0||strcmp(e->d_name,".keep")==0)continue;char child[1024];if(snprintf(child,sizeof child,"%s/%s",path,e->d_name)>=(int)sizeof child){closedir(d);return -1;}struct stat st;if(lstat(child,&st)!=0){closedir(d);return -1;}if(S_ISDIR(st.st_mode)){if(walk(child,depth+1,s)!=0){closedir(d);return -1;}}else if(S_ISREG(st.st_mode)){s->files++;s->bytes+=st.st_size;if(depth>s->depth)s->depth=depth;if(st.st_size>s->largest)s->largest=st.st_size;size_t n=strlen(e->d_name);if(n>=4&&strcmp(e->d_name+n-4,".txt")==0)s->text++;if(n>=2&&strcmp(e->d_name+n-2,".c")==0)s->sources++;}}closedir(d);return 0;}"""
    return f"""#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
struct summary{{long long files,bytes,depth,text,dirs,largest,sources;}};
{walk}
int main(int argc,char**argv){{if(argc!=2)return 1;struct summary s={{0}};if(walk(argv[1],0,&s)!=0)return 1;printf("result: %lld\\n",(long long)({result_body}));return 0;}}
"""


def _tree_questions() -> Iterable[AuthoredQuestion]:
    difficulties = (3, 3, 4, 4, 4, 4, 4)
    for index, (key, title, op, result, tags, _) in enumerate(TREE_OPERATIONS, start=1):
        difficulty = difficulties[index - 1]

        def run(case: Case, operation: Callable[[Case], int] = op) -> tuple[str, str, int]:
            return f"result: {operation(case)}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1521-tree-{index:03d}",
            title=title,
            course="COMP1521",
            kind="c_program",
            difficulty=difficulty,
            track="challenge" if difficulty >= 4 else "normal",
            tags=tags,
            weeks=(8, 9),
            slot="advanced_systems",
            minutes=24 + difficulty * 5,
            background="A build/archive inspection tool must walk a supplied directory tree. Only real regular files and real directories participate; traversal order must not affect the scalar result.",
            requirements="Accept one root directory, recursively traverse it, and print the computed value as `result: X` followed by one newline. The root directory has depth zero and counts as a directory for directory-count questions. Ignore any file named `.keep`; it is used only to create an otherwise empty test directory.",
            implementation_notes="Skip `.` and `..`, construct bounded child paths, call `lstat`, and close every opened `DIR *` even on failure.",
            idea=f"Use depth-first traversal and merge each entry into a summary for {title.lower()}.",
            steps=(
                "Open the current directory and count/initialise its summary.",
                "Skip dot entries and classify each child with `lstat`.",
                "Recurse into directories and update file metrics exactly once for regular files.",
                "Close the directory and print the requested summary field.",
            ),
            correctness="Induction on the directory tree shows that each recursive call accounts for every regular file and subdirectory in its subtree exactly once. Combining those disjoint summaries yields the correct root metric.",
            complexity="Traversal is `O(e)` in the number of entries, with call-stack/path space proportional to maximum depth.",
            pitfalls="Do not recurse into `.`/`..`, count the same file twice, use the process working directory instead of the argument, or leak a directory stream after an error.",
            starter=_tree_source(result, starter=True),
            reference=_tree_source(result, starter=False),
            cases=TREE_CASES,
            oracle=run,
            definition=TREE_DEFINITIONS[key],
        )


THREAD_CASES = SEQUENCE_CASES


THREAD_OPERATIONS = (
    ("sum", "Mutex-Protected Sensor Sum", sum, 0),
    ("positive", "Threaded Positive Count", lambda a: sum(x > 0 for x in a), 1),
    ("even", "Threaded Even Count", lambda a: sum(x % 2 == 0 for x in a), 2),
    ("absolute", "Threaded Absolute Total", lambda a: sum(abs(x) for x in a), 3),
    (
        "weighted",
        "Threaded Weighted Checksum",
        lambda a: sum((i + 1) * x for i, x in enumerate(a)),
        4,
    ),
)

REDUCTION_DEFINITIONS = {
    "sum": "Return the sum of all input elements, or 0 for an empty array.",
    "positive": "Count input elements strictly greater than zero; zero does not count.",
    "even": "Count input elements divisible by two, including zero and negative even values.",
    "absolute": "Return the sum of the absolute values of all input elements.",
    "weighted": "Compute `sum((i + 1) * a[i])` with one-based position weights.",
}


def _thread_source(mode: int, *, starter: bool) -> str:
    worker_body = (
        "(void)arg;(void)lock;return NULL;"
        if starter
        else """struct job*j=arg;long long local=0;for(int i=j->start;i<n;i+=3){int x=values[i];if(MODE==0)local+=x;else if(MODE==1)local+=x>0;else if(MODE==2)local+=(x&1)==0;else if(MODE==3)local+=x<0?-(long long)x:x;else local+=(long long)(i+1)*x;}pthread_mutex_lock(&lock);total+=local;pthread_mutex_unlock(&lock);return NULL;"""
    )
    return f"""#include <pthread.h>
#include <stdio.h>
#define MODE {mode}
static int values[100],n;static long long total;static pthread_mutex_t lock=PTHREAD_MUTEX_INITIALIZER;
struct job{{int start;}};
static void*worker(void*arg){{{worker_body}}}
int main(void){{if(scanf("%d",&n)!=1||n<0||n>100)return 1;for(int i=0;i<n;i++)if(scanf("%d",&values[i])!=1)return 1;pthread_t t[3];struct job j[3];for(int i=0;i<3;i++){{j[i].start=i;if(pthread_create(&t[i],NULL,worker,&j[i])!=0)return 1;}}for(int i=0;i<3;i++)if(pthread_join(t[i],NULL)!=0)return 1;pthread_mutex_destroy(&lock);printf("result: %lld\\n",total);return 0;}}
"""


def _thread_questions() -> Iterable[AuthoredQuestion]:
    for index, (key, title, op, mode) in enumerate(THREAD_OPERATIONS, start=1):

        def run(case: Case, operation: Callable[[list[int]], int] = op) -> tuple[str, str, int]:
            return f"result: {operation(_values(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1521-thread-{index:03d}",
            title=title,
            course="COMP1521",
            kind="c_program",
            difficulty=4,
            track="challenge",
            tags=("threads", "synchronisation", "c-revision", "integer-representation"),
            weeks=(10,),
            slot="processes_threads",
            minutes=32,
            background="Three worker threads process disjoint stride-three positions of a bounded sensor array. They merge local results under one mutex so output remains deterministic.",
            requirements="Read `n` and `n` integers. The supplied `main` creates exactly three workers. Worker `start` processes indices `start, start + 3, ...`; each worker computes a local value, locks once to merge it, and returns. After all joins the program prints `result: X`.",
            implementation_notes="Pass stable job records, compute locally before locking, check thread calls, and destroy the mutex after all joins.",
            idea=f"Partition indices by residue modulo three and merge local values for {title.lower()} under a mutex.",
            steps=(
                "Read the array before creating threads.",
                "Create three stable jobs with distinct start indices.",
                "Compute each local result without shared writes, then lock once to merge.",
                "Join every thread before printing and destroying the mutex.",
            ),
            correctness="The three residue classes are disjoint and cover every array index. Each worker computes the exact metric contribution of its class; mutex-serialised addition loses no contribution, so the joined total equals the full metric.",
            complexity="Total work is `O(n)`, shared storage is `O(n)`, and each worker locks once.",
            pitfalls="Do not pass the address of a changing loop variable, print before joins, hold the mutex for the whole scan, or forget that empty classes are valid.",
            starter=_thread_source(mode, starter=True),
            reference=_thread_source(mode, starter=False),
            cases=THREAD_CASES,
            oracle=run,
            build_flags=("-pthread",),
            definition=REDUCTION_DEFINITIONS[key],
        )


PROCESS_OPERATIONS = (
    ("sum", "Pipe-Transferred Child Sum", sum, 0),
    ("positive", "Pipe-Transferred Positive Count", lambda a: sum(x > 0 for x in a), 1),
    ("even", "Pipe-Transferred Even Count", lambda a: sum(x % 2 == 0 for x in a), 2),
    ("absolute", "Pipe-Transferred Absolute Total", lambda a: sum(abs(x) for x in a), 3),
    (
        "weighted",
        "Pipe-Transferred Weighted Checksum",
        lambda a: sum((i + 1) * x for i, x in enumerate(a)),
        4,
    ),
)


def _process_source(mode: int, *, starter: bool) -> str:
    child = (
        "/* TODO: compute and write one complete result record. */(void)values;return 1;"
        if starter
        else """long long result=0;for(int i=0;i<n;i++){int x=values[i];if(MODE==0)result+=x;else if(MODE==1)result+=x>0;else if(MODE==2)result+=(x&1)==0;else if(MODE==3)result+=x<0?-(long long)x:x;else result+=(long long)(i+1)*x;}if(write(p[1],&result,sizeof result)!=(ssize_t)sizeof result)_exit(2);close(p[1]);_exit(0);"""
    )
    return f"""#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#define MODE {mode}
int main(void){{int n,values[100];if(scanf("%d",&n)!=1||n<0||n>100)return 1;for(int i=0;i<n;i++)if(scanf("%d",&values[i])!=1)return 1;int p[2];if(pipe(p)!=0)return 1;pid_t pid=fork();if(pid<0)return 1;if(pid==0){{close(p[0]);{child}}}close(p[1]);long long result;if(read(p[0],&result,sizeof result)!=(ssize_t)sizeof result)return 1;close(p[0]);int status;if(waitpid(pid,&status,0)<0||!WIFEXITED(status)||WEXITSTATUS(status)!=0)return 1;printf("result: %lld\\n",result);return 0;}}
"""


def _process_questions() -> Iterable[AuthoredQuestion]:
    for index, (key, title, op, mode) in enumerate(PROCESS_OPERATIONS, start=1):

        def run(case: Case, operation: Callable[[list[int]], int] = op) -> tuple[str, str, int]:
            return f"result: {operation(_values(case))}\n", "", 0

        yield AuthoredQuestion(
            id=f"c1521-pipeline-{index:03d}",
            title=title,
            course="COMP1521",
            kind="c_program",
            difficulty=5,
            track="challenge",
            tags=("processes", "pipes", "binary-data", "file-io", "c-revision"),
            weeks=(7, 10),
            slot="challenge_combo",
            minutes=42,
            background="A parent delegates one deterministic reduction to a child. Because post-fork memory is private, the child returns a fixed-width binary result record through a pipe.",
            requirements="Read `n` and `n` integers. The supplied code creates a pipe and forks one child. Complete the child branch so it computes the required value, transfers one `long long`, closes its pipe end, and exits successfully. The parent waits and prints `result: X`.",
            implementation_notes="Close unused pipe ends immediately, require full record transfer, use `_exit` in the child, and validate `waitpid` status.",
            idea=f"Compute {title.lower()} in the child and use the pipe as the only result channel back to the parent.",
            steps=(
                "Read all data before `fork` and create the pipe.",
                "Close opposite pipe ends in parent and child.",
                "Compute and write one fixed-size result, then `_exit(0)`.",
                "Read the full record, wait for success, and print in the parent.",
            ),
            correctness="The child applies the metric to the inherited immutable array and writes exactly that scalar. The parent prints only the complete record after confirming child success, so the observable result equals the specified reduction.",
            complexity="The child performs `O(n)` work; pipe traffic and extra storage are `O(1)` beyond the input array.",
            pitfalls="Do not expect shared memory after `fork`, leave both writers open, accept a short read/write, call buffered `exit` in the child, or ignore child status.",
            starter=_process_source(mode, starter=True),
            reference=_process_source(mode, starter=False),
            cases=SEQUENCE_CASES,
            oracle=run,
            definition=REDUCTION_DEFINITIONS[key],
        )


def comp1521_questions() -> tuple[AuthoredQuestion, ...]:
    questions = tuple(
        (
            *_bit_questions(),
            *_mips_questions(),
            *_file_questions(),
            *_unicode_questions(),
            *_tree_questions(),
            *_thread_questions(),
            *_process_questions(),
        )
    )
    if len(questions) != 75:
        raise AssertionError(f"expected 75 COMP1521 questions, found {len(questions)}")
    return questions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", choices=("comp1511", "comp1521", "all"), default="all")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    questions = (
        (*comp1511_questions(), *comp1521_questions())
        if args.course == "all"
        else comp1511_questions()
        if args.course == "comp1511"
        else comp1521_questions()
    )
    written = sum(_emit(question, refresh=args.refresh) for question in questions)
    print(f"wrote {written} questions; catalogue contains {len(questions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
