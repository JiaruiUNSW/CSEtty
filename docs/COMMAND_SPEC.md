# Command compatibility specification

Status: implemented public-alpha contract, schema/profile version 1

All command output is original CSEExamTTY wording. The goal is behavioural
familiarity, not an exact copy of a term-specific UNSW script.

## 1. Host CLI

```text
csetty doctor [--offline-ready PROFILE]
csetty prepare --profile comp1511|comp1521|all [--mipsy-source PATH]
csetty packs list
csetty pack validate PATH
csetty pack verify PATH --reference PATH
csetty start PACK [--mode practice|exam] [--editor code|terminal]
                  [--workspace PATH] [--network none|on]
                  [--timed] [--skip-reading]
csetty resume [ATTEMPT_ID]
csetty code [ATTEMPT_ID]
csetty page [ATTEMPT_ID]
csetty export ATTEMPT_ID DESTINATION
csetty attempts list
csetty report [ATTEMPT_ID] [--json]
csetty bank validate PATH
csetty bank stats PATH
csetty bank verify PATH
csetty bank build PATH DESTINATION --seed INTEGER [--version X.Y.Z]
```

Defaults are practice mode, the isolated VS Code editor, a Docker volume
workspace, no network, and no practice timer. `--timed` uses the pack's working
time. There is no pause operation in schema/profile version 1.

Exam mode is always timed. It rejects `--network on` and `--skip-reading`.
Practice mode remains offline unless networking is explicitly enabled. Start
and resume never pull an image, VS Code Server, or extension.

### Preparation

`prepare` source-builds and records local interactive and judge images, then
prepares application-owned VS Code caches. COMP1521 uses the independent pinned
`csetty-mips` dependency and does not require an upstream checkout. The optional
`--mipsy-source` argument validates and records a clean pinned checkout for
private black-box comparison only; it is never used in the course image.
Preparation may use the network; attempts do not.

### Workspace selection

Without `--workspace`, a persistent named Docker volume is created. A supplied
bind directory must be empty except for `.DS_Store`. Starter initialization is
refused rather than overwriting content in a non-empty new bind directory.

### Attempt selection

`resume`, `code`, and `page` accept a full attempt UUID or an unambiguous prefix.
With no argument, they select the most recent active attempt. `page` starts or
reuses the loopback-only exam companion; it does not restart the attempt.
`report` also accepts a full UUID or unambiguous prefix; with no argument, it
selects the newest attempt, including a finished or expired attempt.

The `bank` commands validate original source questions, report coverage, verify
all reference implementations in the real judge, or build a deterministic
100-mark exam pack. See `QUESTION_BANK.md` for the schema and fixed course
blueprints.

## 2. Exam entry gate

Only `csetty start ... --mode exam` runs the entry gate. It occurs in the host
terminal before an attempt record, reading view, workspace, container, or VS
Code window is created. After startup prerequisites pass, CSEExamTTY clears the
interactive terminal's visible screen and scrollback before drawing the gate;
redirected non-TTY output is left unchanged.

The visible sequence after that clear is:

1. `Welcome to the COMPxxxx Exam Simulation`;
2. a lowercase `z` followed by exactly seven digits;
3. any non-empty simulation-only password;
4. a declaration that the system is neither made nor managed by UNSW CSE;
5. an original academic-integrity and examination-conditions summary; and
6. exact acknowledgement with `yes`.

The password is deliberately discarded in memory and is never authenticated,
stored, hashed, logged, or included in an event or report. Declining the
conditions creates no attempt.

## 3. Commands inside every working attempt

```text
exam help
exam status
exam questions
exam submissions [ACTIVITY]
exam finish [--yes]
check
```

- `exam status` displays pack, course, candidate/practice user, mode, state,
  remaining time, UTC deadline, image, and the local-only destination notice.
- `exam questions` reports `NOT STARTED`, `MODIFIED`, `TESTED`, `SUBMITTED`, or
  `SUBMITTED (unsubmitted changes)` for every question.
- `exam submissions` lists every accepted sequence, timestamp, manifest hash,
  and the latest sequence without claiming UNSW receipt.
- `exam finish` requires terminal confirmation; non-TTY callers must pass
  `--yes`. It makes the attempt terminal, grades latest accepted snapshots, and
  warns when a question has no accepted submission. It writes the JSON and HTML
  reports, opens the HTML report in the host's default browser, and prints the
  local HTML path plus the matching host `csetty report` command. Browser launch
  failure never invalidates the completed attempt or generated reports. The
  HTML report uses the same packaged COMP1511/COMP1521 course theme as the live
  paper; it does not depend on remote CSS or JavaScript.

Closing Bash or VS Code is not finish. A timed deadline continues.

## 4. COMP1511 profile

```text
1511 fetch [ACTIVITY]
1511 autotest ACTIVITY [TEST_SELECTOR]
autotest ACTIVITY [TEST_SELECTOR]
submit ACTIVITY [FILE ...]
1511 check
check
```

With no activity, `1511 fetch` restores every missing starter. With an activity,
it handles only that question. Existing regular files are retained. The private
prototype also accepts `--force` in practice mode for an explicit atomic
restore; exam mode rejects it.

`submit ACTIVITY` resolves the manifest files. Explicit filenames are accepted
only when their set exactly equals the declared submission set. `q1`, `q2`, and
so on are short aliases for the questions in pack order.

## 5. COMP1521 profile

```text
1521 fetch PACK
1521 autotest ACTIVITY [TEST_SELECTOR]
1521 mipsy FILE [ARG ...]
submit ACTIVITY [FILE ...]
1521 check
check
1521 classrun -check
1521 classrun ACTIVITY
```

`1521 classrun check` is also accepted as a compatibility alias.
`1521 classrun ACTIVITY` prints the latest accepted answer with the question,
filename, candidate, UTC submission time, and source line numbers.
`1521 mipsy FILE ARG...` invokes the image's local `csetty-mips` runner and
inserts the runner's `--` argument separator without using a shell. Supplying an
explicit `--` is also accepted. The direct `mipsy` command retains its full
`mipsy [OPTIONS] FILE... [-- PROGRAM_ARG...]` interface.

For both profiles, successful submission output is exactly one line:

```text
Your answer (FILE) for q1 has been submitted.
```

`check`, `1511 check`, `1521 check`, and `1521 classrun -check` use the same
two-line summary:

```text
You have submissions for following questions:
q1 q2
```

## 6. Autotest behaviour

Autotest never submits. It:

1. validates the active attempt, activity, and optional public group/test
   selector;
2. reads only the declared regular answer files without following symlinks;
3. creates an immutable snapshot separate from the live workspace;
4. starts an ephemeral, offline, resource-limited judge;
5. compiles once using the manifest argument array;
6. runs every selected test in a clean directory; and
7. persists a structured test run.

Student-facing output includes the compiler check/command, then lines in this
form:

```text
Test positive_0 (./answer) - passed
Test negative_0 (./answer) - failed (incorrect output)
```

An incorrect stream prints the actual output, expected output, a unified diff,
stdin, and copyable build/run commands. The final line is:

```text
N tests passed M tests failed
```

`passed`, individual failures, and an all-passing summary are coloured in an
interactive TTY. Redirected output and any environment containing `NO_COLOR`
have no ANSI escapes.

Stable result classes are:

```text
PASS
COMPILE_ERROR
WRONG_OUTPUT
WRONG_EXIT_STATUS
RUNTIME_ERROR
TIMEOUT
OUTPUT_LIMIT
INTERNAL_ERROR
```

An `INTERNAL_ERROR` is a simulator/pack failure, not a student failure.

## 7. Submission and grading semantics

- The host snapshots, hashes, and durably records declared files before success
  is returned.
- Every submission receives a per-question increasing sequence number.
- Historical versions remain available; only the latest accepted sequence per
  question is used for final grading.
- The final grade never reads the live workspace.
- A transaction rechecks state and deadline immediately before acceptance.
- A timestamp at or after the deadline is rejected.
- Public autotests have no effect on submission acceptance.
- Test-group points are all-or-nothing; `pass_points` determines question pass,
  and cross-question hurdles are evaluated afterward.

## 8. Timing semantics

During reading time, the host terminal shows the paper index/countdown and the
loopback-only companion shows every complete prompt plus explicitly permitted
bundled resources. There is no workspace or editable container on which to run
a command. The live countdown uses a monotonic clock. The reading anchor and
working deadline are persisted as UTC timestamps so a restart cannot grant more
time. The open page detects the transition to working state and refreshes
without opening a duplicate browser tab.

The supervisor checks expiry before operations and while polling. A timed expiry
uses the same final grading, report-writing, and browser-opening path as an
explicit finish. Once an attempt is `FINISHED`, `EXPIRED`, or `ABORTED`, it is
immutable.

## 9. Exit codes

| Code | Meaning |
|---:|---|
| 0 | Operation completed successfully |
| 1 | Valid autotest request completed with one or more student failures |
| 2 | Invalid command usage |
| 3 | Attempt state or deadline forbids the operation |
| 4 | Required host/container tool is unavailable |
| 5 | Pack validation or simulator internal error |

## 10. Compatibility boundaries

Ordinary shell commands come from Debian and are not parsed by CSEExamTTY.
`la` is not included because it is a user-defined alias; `ls -la` is portable.
Output avoids UNSW logos and always describes submissions and marks as local.
