# Original question banks

Status: schema v1 implemented; 300 original questions included in the source
checkout. Every question has at least five distinct public/after-finish test
points and a worked, step-by-step solution.

## Inventory

| Bank | Questions | Tracks | Difficulty | Generated paper |
|---|---:|---|---|---|
| `question_bank/comp1511` | 150 | normal/challenge | 1–5 | 11 questions, 100 marks |
| `question_bank/comp1521` | 150 | normal/challenge | 1–5 | 10 questions, 100 marks |

Each question directory contains `question.json`, `prompt.md`, `solution.md`,
one or more starter files, matching author reference files, and public and
`after_finish` tests. Prompts must include Background, Requirements, Examples,
and Implementation notes. Solutions must include Approach, Step-by-step, Worked
example, Correctness, Complexity, and Common pitfalls.

Student-facing prompts must state the concrete operation directly; a title or
scenario must never be the only definition of the task. When starter code
contains a marked function or block, the prompt names that exact editable
interface and explains what the supplied `main` already does. Examples use
fenced input/output blocks and show command arguments or fixture contents only
when they exist. Author provenance, hidden-marking language, and internal build
details do not belong in a student prompt.

The generated half of each bank is reproduced by
`scripts/generate_question_bank_expansion.py`. The older half is normalised by
`scripts/polish_legacy_question_prompts.py`; both scripts are idempotent so a
curator can refresh the committed Markdown without changing tests or scoring.

## Fixed papers, banks, and generated papers

These names are intentionally different:

| Name | What it is | What to do with it |
|---|---|---|
| `comp1511-original-a` | A fixed 11-question exam paper | Start it directly with `csetty start comp1511-original-a --mode exam` |
| `comp1521-original-a` | A fixed 10-question exam paper | Start it directly with `csetty start comp1521-original-a --mode exam` |
| `comp1511` | The built-in 150-question COMP1511 bank | Pass it to `csetty bank build`; do not pass it directly to `csetty start` |
| `comp1521` | The built-in 150-question COMP1521 bank | Pass it to `csetty bank build`; do not pass it directly to `csetty start` |

Build a paper into a new or empty directory, then run that directory through
the normal exam workflow:

```sh
csetty bank build comp1511 ./my-comp1511-paper --seed 1511
csetty start ./my-comp1511-paper
```

Generated papers default to exam mode, so the second command shows the Welcome
screen and simulated zID entry before the read-only reading period without an
extra flag. The starter workspace is created only when working time begins. Use
`--mode practice` only to opt out explicitly. Generated filenames are based on
exam position (`q1.c`, `q2.c`, and so on; MIPS questions use `qN.s`), so the
normal `autotest q1` and `submit q1` workflow applies. Using the same bank
version and seed reproduces the same paper; changing the seed requests a
different selection.

## Commands

```text
csetty bank validate PATH
csetty bank stats PATH
csetty bank verify PATH
csetty bank build PATH DESTINATION --seed INTEGER [--version X.Y.Z]
```

`PATH` may be a custom bank directory or the built-in selector `comp1511` or
`comp1521`. The built-in banks are included in both source and wheel installs.

Validation checks the manifest, topic and slot vocabularies, IDs, paths, prompt
and solution structure, starter/reference coverage, build commands, tests,
weights, and all ordinary exam-pack invariants. A build is deterministic for a
given bank, seed, and version. `DESTINATION` must be absent or empty.

The bundled manifests additionally require five or more test points per
question, full coverage of every allowed topic tag in each generated paper, and
an exact non-decreasing difficulty pattern. Selection uses deterministic
backtracking rather than independent per-slot choices, so all three constraints
hold together for every valid seed.

`bank verify` creates a temporary author-only pack containing every question,
then runs every reference implementation against every public and
`after_finish` test through the same offline, resource-limited Docker judge used
for final grading. The temporary pack is removed after verification.

## Question JSON

Question files use the regular pack question/test-group contract plus:

```json
{
  "schema_version": 1,
  "id": "c1521-example-001",
  "title": "Original title",
  "kind": "c_program",
  "difficulty": 3,
  "track": "normal",
  "tags": ["file-io"],
  "weeks": [8],
  "slots": ["advanced_systems"],
  "estimated_minutes": 20,
  "prompt": "prompt.md",
  "solution": "solution.md"
}
```

The full object also contains points, pass threshold, starter/submission files,
shell-free build argv, and test groups. Allowed tags and slots are declared in
the course `bank.toml`; unknown values fail validation.

## COMP1511 blueprint

| Position | Slot | Marks |
|---|---|---:|
| Q1, Q3 | linked-list hurdle | 12 each |
| Q2, Q4 | array hurdle | 12 each |
| Q5–Q8 | short lab/debugging/function questions | 5 each |
| Q9–Q10 | medium questions | 11 each |
| Q11 | whole program | 10 |

Generated packs include linked-list and array cross-question hurdles. The bank
covers conditions, loops, functions, arrays, strings, structs, pointers,
dynamic memory, linked lists, recursion, debugging, character streams, and
whole-program work.

## COMP1521 blueprint

| Position | Slot | Marks |
|---|---|---:|
| Q1 | foundation file-I/O question | 10 |
| Q2 | foundation bitwise/integer-representation question | 10 |
| Q3 | foundation MIPS translation/control/data/function question | 10 |
| Q4 | another foundation lab/weekly-test-level question | 10 |
| Q5 | Unicode | 10 |
| Q6–Q8 | advanced systems, MIPS, files, metadata, or recursive traversal | 10 each |
| Q9 | processes or threads | 10 |
| Q10 | challenge combination | 10 |

Q10 is always selected from the challenge track. The bank includes one
or more floating-point questions, and every generated paper covers the
`floating-point` tag together with all other declared COMP1521 tags.

## Difficulty progression

| Bank | Difficulty by position |
|---|---|
| COMP1511 | 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5 |
| COMP1521 | 1, 1, 2, 2, 3, 3, 4, 4, 4, 5 |

Repeated levels are intentional where a paper has more positions than the five
difficulty levels. A later question is never easier than an earlier one, and
each paper spans at least three levels.

## Generated-pack isolation

Only starter files, question prompts, and declared student resources are placed
in the assessed pack. Worked solutions and reference source are copied under
`solutions/`, then frozen into the attempt's separate author snapshot. They are
not mounted into the interactive or judge container and appear only after the
attempt is finished or expired.

All content is original local-simulation material. Course pages inform topic
coverage and assessment shape only; the generator does not download or copy
UNSW question text.
