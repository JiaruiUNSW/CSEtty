# CSEExamTTY original question bank

This directory contains original local-simulation questions. It does not contain
UNSW examination questions, copied lab text, UNSW branding, or confidential
assessment material. Public course pages are used only to identify the taught
topic taxonomy and the broad shape of normal and challenge exercises.

The current inventory is 150 COMP1511 questions and 150 COMP1521 questions (300
total). Every difficulty level 1–5 and both tracks are represented in each
course bank. Every question declares at least five distinct test points.

## Per-course layout

```text
comp1511/
├── bank.toml
└── questions/
    └── c1511-arrays-001/
        ├── question.json
        ├── prompt.md
        ├── solution.md
        ├── starter/
        │   └── c1511_arrays_001.c
        └── reference/
            └── c1511_arrays_001.c
```

Fixtures referenced by tests live below the same question directory. All paths
in `question.json` are relative to that directory. A question must be entirely
self-contained and use unique submission filenames.

## `question.json` schema v1

```json
{
  "schema_version": 1,
  "id": "c1511-arrays-001",
  "title": "Original question title",
  "kind": "c_program",
  "difficulty": 2,
  "track": "normal",
  "tags": ["arrays-1d", "loops"],
  "weeks": [4],
  "slots": ["array_hurdle"],
  "estimated_minutes": 18,
  "points": 12,
  "pass_points": 6,
  "prompt": "prompt.md",
  "solution": "solution.md",
  "starter_files": ["starter/c1511_arrays_001.c"],
  "submission_files": ["c1511_arrays_001.c"],
  "build": {"argv": ["dcc", "-Werror", "c1511_arrays_001.c", "-o", "c1511_arrays_001"]},
  "test_groups": []
}
```

`test_groups` uses the pack schema-v1 test representation. Every question must
have at least one `public` group and one `after_finish` group. All group points
must sum to the question points, and passing the reference program must be
sufficient to earn every point. The bundled manifests set
`minimum_test_points = 5`; validation rejects a question below that floor.

Difficulty is an integer from 1 to 5. `track` is either `normal` or
`challenge`. Tags and slot values must be declared by the course's `bank.toml`.

Every `prompt.md` must contain these exact headings:

- `## Background`
- `## Requirements`
- `## Examples`
- `## Implementation notes`

Every `solution.md` must contain:

- `## Approach`
- `## Step-by-step`
- `## Worked example`
- `## Correctness`
- `## Complexity`
- `## Common pitfalls`

The prompt should be detailed enough to stand alone. It must specify the exact
interface, inputs, outputs, assumptions, restrictions, examples, and submission
filename. The solution should explain the algorithm and not merely restate the
reference source.

## Exam blueprints

The COMP1511 generator fills 11 slots: two linked-list hurdles, two array
hurdles, four short questions, two medium questions, and one whole-program
question. Their marks are 12, 12, 12, 12, 5, 5, 5, 5, 11, 11, and 10.

The COMP1521 generator fills 10 ten-mark slots:

- Q1-Q4: foundation questions drawn from files, bitwise operations, MIPS
  translation, and other normal lab/weekly-test material;
- Q5: Unicode/UTF-8;
- Q6-Q8: advanced systems questions, including harder versions of early topics
  and possible recursive directory traversal;
- Q9: processes or threads; and
- Q10: a challenge combination, including processes, pipes, threads, or
  synchronisation.

`csetty bank build` chooses deterministically from these slots when given a
seed. It solves the whole blueprint jointly: the selected questions must cover
every `required_coverage_tags` entry, remain unique, and match the manifest's
non-decreasing `difficulty_pattern`. The current patterns are
`1,1,2,2,2,2,3,3,4,4,5` for COMP1511 and
`1,1,2,2,3,3,4,4,4,5` for COMP1521. Generated papers remain local estimates
and never imply UNSW endorsement.
