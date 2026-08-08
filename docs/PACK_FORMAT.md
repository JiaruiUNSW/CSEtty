# Exam-pack format

Status: implemented TOML schema version 1

Packs contain original or licensed paper text, starter files, permitted
resources, test fixtures, scoring metadata, and an optional author-only
reference-solution tree. They select a trusted course profile; they cannot
inject Docker flags, mounts, capabilities, networks, or host paths.

## 1. Layout

```text
comp1511-original-a/
├── pack.toml
├── paper/
│   ├── index.md
│   └── questions/
│       └── prac_q1.md
├── starter/
│   └── prac_q1.c
├── resources/
│   └── c-reference.md
├── tests/
│   └── fixtures...
└── solutions/
    ├── explanations/
    │   └── prac_q1.md
    └── reference/
        └── prac_q1.c
```

`solutions/` is authoring material. It is excluded from the student pack
digest, student workspace, interactive container, and sanitized judge mount.
At attempt creation it is copied into a read-only author snapshot with its own
SHA-256 manifest so a finished report can show the exact worked solution used
for that attempt. A fully local `after_finish` fixture or author snapshot still
cannot be considered secret from the owner of the host computer.

## 2. Minimal manifest

```toml
schema_version = 1
id = "comp1511-original-example"
version = "1.0.0"
title = "Original Practice Example"
course = "COMP1511"
profile = "comp1511"
author = "Example author"
license = "CC BY-NC-ND 4.0"
paper = "paper/index.md"
default_mode = "practice"
reading_time_seconds = 600
working_time_seconds = 10800

[environment]
image = "csetty/comp1511:dev"
network = "none"
cpus = 2
memory_mb = 1024
pids = 128
output_limit_kb = 256

[[resources]]
path = "resources/c-reference.md"
label = "C quick reference"

[[questions]]
id = "prac_q1"
title = "Count adjacent increases"
kind = "c_program"
prompt = "paper/questions/prac_q1.md"
difficulty = 2
track = "normal"
tags = ["arrays-1d", "loops"]
estimated_minutes = 15
points = 10
pass_points = 5
starter_files = ["starter/prac_q1.c"]
submission_files = ["prac_q1.c"]

[questions.build]
argv = ["dcc", "-Werror", "prac_q1.c", "-o", "prac_q1"]

[[questions.test_groups]]
id = "public"
visibility = "public"
points = 5

[[questions.test_groups.tests]]
id = "small"
argv = ["./prac_q1"]
stdin = "3\n1 2 3\n"
expected_stdout = "2\n"
expected_stderr = ""
expected_exit = 0
timeout_ms = 2000
comparison = "exact"

[[questions.test_groups]]
id = "marking"
visibility = "after_finish"
points = 5

[[questions.test_groups.tests]]
id = "boundary"
argv = ["./prac_q1"]
stdin = "1\n7\n"
expected_stdout = "0\n"
expected_stderr = ""
expected_exit = 0

[[hurdles]]
id = "array_hurdle"
label = "Array hurdle"
question_ids = ["prac_q1"]
min_passed_questions = 1
```

## 3. Top-level contract

| Field | Rule |
|---|---|
| `schema_version` | Exactly `1` |
| `id` | Lowercase stable identifier |
| `version` | Semantic version form `X.Y.Z` |
| `title` | Non-empty display title |
| `course` | Display course, normally `COMP1511` or `COMP1521` |
| `profile` | `comp1511` or `comp1521` |
| `author` | Content author/organisation |
| `license` | Non-empty license label; bundled original packs use `CC BY-NC-ND 4.0` |
| `paper` | Existing UTF-8 Markdown path under the pack root |
| `default_mode` | Optional `practice` or `exam`; defaults to `practice` for ordinary packs |
| `reading_time_seconds` | Non-negative integer |
| `working_time_seconds` | Positive integer |

Pack identity is `(id, version, SHA-256 digest)`. Attempts persist the path and
digest and refuse resume when assessed pack content changes.

Papers emitted by `csetty bank build` declare `default_mode = "exam"`, so a
plain `csetty start PATH` runs the Welcome, candidate sign-in, acknowledgement,
reading, and working sequence. `--mode practice` remains an explicit override.
Generated packs created by older CSEExamTTY versions are recognised by their
generated pack identity and receive the same default for compatibility.

## 4. Environment ceilings

The manifest image must match its trusted profile (`csetty/comp1511:dev` or
`csetty/comp1521:dev`) and `network` must be `none`. The host resolves the image
from the profile rather than accepting an arbitrary image reference.

| Field | Allowed schema-v1 value |
|---|---:|
| `cpus` | greater than 0, at most 8 |
| `memory_mb` | 1–4096 |
| `pids` | 1–512 |
| `output_limit_kb` | 1–2048 per captured stream |

Attempt mode may apply a stricter network policy. Exam mode always uses
`--network none`.

## 5. Questions and scoring

Supported `kind` values are `c_program`, `c_function`, `mips_program`, and
`text`. Every question declares:

- exact starter and submission paths;
- total `points` and a `pass_points` threshold;
- a shell-free build argument array (required for C, optionally empty for MIPS
  or text); and
- one or more test groups.

Question presentation metadata is optional for backwards compatibility but is
required by the bundled question banks:

| Field | Rule |
|---|---|
| `prompt` | UTF-8 Markdown path under the pack root; falls back to title-only text when omitted |
| `difficulty` | Integer from 1 (introductory) through 5 (most demanding); default 3 |
| `track` | `normal` or `challenge`; default `normal` |
| `tags` | Unique non-empty topic labels used for navigation and report advice |
| `estimated_minutes` | Optional integer from 1 through 180 |

The companion page renders the prompt and metadata while an attempt is active.
After the attempt reaches a terminal state, the report may also render
`solutions/explanations/QUESTION_ID.md` and matching files under
`solutions/reference/`. These author materials are snapshotted separately at
attempt creation and are never exposed in the student pack.

Group points may sum to less than the question total. The difference is shown
as `not automatically assessed`. They may not exceed the question total, and
`pass_points` may not exceed automatically assessable points.

Group points are divided equally among the group's test points. Each passing
test earns its share; the group itself is marked passed only when every declared
test passes. A question passes when earned automatic points reach
`pass_points`. A hurdle names multiple questions and a required minimum number
of passed questions.

## 6. Tests

A test declares an argument array, optional stdin, expected stdout/stderr/exit,
timeout, comparison, fixtures, and optional expected output files. Expected
streams may be inline or loaded from a pack-relative file, but not both.

Supported comparisons are:

- `exact`;
- `ignore_trailing_whitespace`;
- `ignore_whitespace`;
- `ignore_case`; and
- `selected_characters` with an explicit character set.

Test timeout must be 1–60,000 ms. Commands use an executable allowlist and are
never passed as a host shell string. Every test runs in a clean copy of the
compiled snapshot.

Fixtures use this form:

```toml
[[questions.test_groups.tests.fixtures]]
source = "tests/q3/input.txt"
path = "input.txt"
```

Expected files use exactly one of `content` or `source`:

```toml
[[questions.test_groups.tests.expected_files]]
path = "result.txt"
content = "expected data\n"
```

## 7. Visibility

`public` groups are selectable during a working attempt. `after_finish` groups
run only as part of terminal-state grading. Final grading runs both using the
latest accepted submission snapshot; it never runs against the live workspace.

Visibility controls feedback timing, not local secrecy.

## 8. Validation and reference verification

`csetty pack validate PATH` rejects unsupported schema/profile/image values,
bad identifiers/versions, duplicate IDs, unsafe or escaping paths, missing
files, invalid command arrays, conflicting expected-output sources, shared
submission paths, invalid points/hurdles, unbounded timeouts, and resource
values beyond application ceilings.

`csetty pack verify PATH --reference PATH` executes every public and
after-finish test for every question against matching reference filenames. It
requires the profile image to have been prepared.

The digest covers all regular files except `.git/` and `solutions/`. Symlink
targets used by declared content must remain under the pack root. The judge
receives a fresh sanitized copy that omits author solutions.

## 9. Content rules

- Do not include confidential or unreleased assessment material.
- Public visibility is not permission to copy question text.
- Use original or explicitly licensed questions and resources.
- Do not use UNSW logos or imply endorsement.
- Record third-party licensing before any public distribution.
