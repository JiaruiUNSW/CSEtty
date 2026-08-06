# CSEExamTTY

CSEExamTTY is an independent local alpha that simulates a practical programming
exam workflow for COMP1511- and COMP1521-style practice. It provides an isolated
Linux shell, original exam packs, course-like commands, immutable submissions,
timed attempts, an ephemeral judge, and local reports.

It is not made, managed, endorsed, or authenticated by UNSW or the UNSW School
of Computer Science and Engineering. It never connects to UNSW systems, and no
local submission is an official submission.

## Current status

The source tree is the `0.1.0a3` source-only alpha release candidate; `0.1.0a1`
remains the latest published alpha. On the current Apple Silicon Mac, both
current course images have passed fresh offline VS Code preparation and attach
checks plus companion, autotest, submission, finish, judge, and report
workflows. COMP1521 uses the separately released `csetty-mips` dependency; no
upstream mipsy binary or source is included in its course image. The alpha
includes:

- COMP1511: 11 original questions, 100 points, DCC/GCC/Clang, arrays, linked
  lists, debugging, functions, and whole programs;
- COMP1521: 10 original questions, 100 points, C, MIPS, POSIX file I/O,
  Unicode, processes, pipes, and threads;
- two original 75-question banks (150 questions total), with normal/challenge
  tracks, difficulty 1–5, topic/week tags, worked solutions, reference programs,
  public tests, and post-finish tests; all 150 reference programs pass every
  declared test in the real isolated judge;
- a 10-minute read-only reading period and 180-minute working period;
- Docker volume workspaces by default, with an opt-in empty bind directory;
- public autotests and post-finish test groups with weighted all-or-nothing
  group scoring and cross-question hurdles;
- repeated, SHA-256-addressed local submissions and JSON/HTML/text reports;
- non-root, read-only-rootfs interactive and judge containers with no Docker
  socket, dropped capabilities, resource limits, and no network by default; and
- an isolated host VS Code instance attached to the interactive container after
  an explicit per-image `prepare` step;
- a loopback-only companion page opened as a full read-only paper during reading
  time and reused beside VS Code during working time, with detailed question
  pages, bundled references, live state/countdown, and an **Open VSC** recovery
  button when working; and
- a post-exam HTML report that opens automatically after an explicit finish or
  timed expiry and contains each submitted source file, detailed test evidence,
  worked solution, reference implementation, strengths, gaps, and targeted
  revision advice.

The repository publishes Python/project source, original assessment materials,
Compose/Dockerfile definitions, and integrity locks only. `prepare` builds
separate interactive/judge images locally and records their exact IDs. Neither
the project nor its CI publishes course images, registry layers, BuildKit
caches, DCC binaries, Debian package archives, VS Code Server, or VSIX caches.
This alpha is locally accepted on Apple Silicon; the checked-in CI matrix is the
release evidence for host Python compatibility and runner-local multi-architecture
source builds. A future stable release still requires broader native desktop,
Docker Desktop/WSL2, and offline VS Code acceptance.

## Install the alpha

Python 3.11 or later and Docker Desktop/Engine are required. VS Code and its
`code` command are required only when using the default editor integration.

```sh
pipx install cseexamtty==0.1.0a1
# or
uv tool install cseexamtty==0.1.0a1
```

Then run `csetty doctor`. `csetty prepare` is the explicit networked phase that
locally builds the course images and warms an isolated VS Code cache.

## Development setup

For development from a source checkout:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/csetty doctor
```

`uv sync --extra dev` may be used instead when `uv` is installed.

## csetty-mips dependency

The independently implemented MIPS32 teaching engine lives in the separate
[CSEtty-MIPS repository](https://github.com/JiaruiUNSW/CSEtty-MIPS) and is
[published on PyPI](https://pypi.org/project/csetty-mips/0.1.1/). This project
pins the `csetty-mips==0.1.1` release as its runtime dependency and records
source commit `33410078667ad67942c6700d73411fc31be00c8f` in its toolchain
locks and image labels. It is the runtime behind `/usr/local/bin/mipsy` and
`1521 mipsy` in the COMP1521 course image, and contains no upstream mipsy
source or binary.

```sh
.venv/bin/csetty-mips program.s -- arg1 arg2
.venv/bin/csetty-mips --check program.s
.venv/bin/csetty-mips --hex-pad-zero program.s
.venv/bin/csetty-mips --interactive program.s
.venv/bin/csetty-mips                 # debugger; use `load FILE...`
```

Strict initialization diagnostics are enabled by default. `--spim` (also
spelled `--relaxed`) makes uninitialized registers and memory read as zero for
compatibility-oriented runs. Sandboxed file syscalls require an explicit
`--fs-root DIR`.

The Python API is also public:

```python
from csetty_mips import Machine, SourceUnit, assemble

program = assemble([SourceUnit("answer.s", ".text\nmain: li $a0, 42\nli $v0, 1\nsyscall\njr $ra\n")])
machine = Machine(program)
machine.run()
assert machine.io.output == b"42"
```

Its package specification, acceptance matrix, clean-room provenance record,
source, and pure-engine tests are maintained in that separate MPL-2.0 project.
This repository retains only CSEExamTTY integration tests and the pinned
dependency contract described in
[the integration note](docs/CSETTY_MIPS_INTEGRATION.md).

Preparation is the only phase that may download or build tooling:

```sh
.venv/bin/csetty prepare --profile comp1511
.venv/bin/csetty prepare --profile comp1521
```

Each preparation uses the digest-pinned Debian 12 multi-architecture base,
downloads the SHA-256-pinned DCC 2.37 source archive and runs its upstream
`make dcc` build locally. It stages the installed external `csetty-mips` source
at its pinned Git commit for COMP1521. No DCC binary, prebuilt course image,
registry layer, public BuildKit cache, VS Code Server, or VSIX cache is shipped
by this repository. `start` verifies the recorded interactive and judge image
IDs and never builds or pulls an image.

`--mipsy-source PATH` remains optional for maintainers who want to validate and
record the pinned upstream checkout used for a private black-box comparison.
That checkout is never copied into, built into, or selected by the course image.

### What preparation does to VS Code

Preparation opens a visibly labelled, isolated **CSEExamTTY** VS Code window.
It uses application-owned `--user-data-dir` and `--extensions-dir` paths. It
does not edit the normal VS Code user settings or normal extension directory.

The isolated window intentionally contains only:

- host side: Dev Containers;
- COMP1511 container: C/C++;
- COMP1521 container: C/C++ and Mipsy Editor Features.

Therefore the Extensions view in that window is not expected to show Python,
Jupyter, ChatGPT, Remote SSH, or any plugin from the normal VS Code profile.
After caching completes, the preparation window moves to a local completion
page before its disposable container is stopped.

## Start an attempt

Practice mode defaults to VS Code, no network, and no timer:

```sh
.venv/bin/csetty start comp1511-original-a
.venv/bin/csetty start comp1521-original-a --editor terminal
```

Exam simulation mode is always timed and offline:

```sh
.venv/bin/csetty start comp1511-original-a --mode exam
```

The exam entry sequence happens in the **host terminal before reading time**:

1. the interactive terminal screen and scrollback are cleared;
2. `Welcome to the COMPxxxx Exam Simulation`;
3. a simulated zID in the form `z` plus seven digits;
4. any non-empty simulation password (never authenticated, stored, hashed, or
   logged; do not enter a real UNSW password);
5. the local-system disclaimer and academic-integrity/exam-condition warning;
6. exact acknowledgement by typing `yes`; and
7. the full read-only paper and reading countdown.

During reading time, the companion page opens in the host browser with every
complete question prompt and only the resources explicitly permitted by the
pack. The persisted reading clock begins only after the companion is healthy
and the browser-launch call succeeds; a reported launch failure leaves the
attempt resumable in `CREATED` state without consuming reading time. That state
serves only a waiting page: complete questions and resources remain unavailable
until a successful `resume` starts the reading clock. No editable container,
workspace, or VS Code window exists yet. When
reading time ends, the same page updates to working state and the starter
workspace, supervised container, and VS Code are opened. A practice attempt,
including one started with `--skip-reading`, deliberately does not show the exam
sign-in gate; the skip choice is persisted if a `CREATED` attempt must be
resumed.

The live paper is a single navigable long-form exam page rather than a
question-name dashboard. Its offline visual shell follows the public CSE course
exam conventions: a course-colour navbar, light examination header, bordered
question headings, Bootstrap-style alerts/tables, and light code/TTY blocks.
COMP1511 uses its green accent and COMP1521 its teal accent. The final HTML
report imports the same local theme, so finishing the exam changes the content
and status, not the course's visual language.

The companion is served only on `127.0.0.1` at an unguessable per-process path.
Its **Open VSC** control reconnects to the existing supervised container and
does not recreate the attempt or reset its clock. Bundled pack references work
offline. Official course links open in the host browser: `--network none`
isolates the Docker container only, so those links remain usable whenever the
host itself has network access. Public course content is not copied into this
repository.

## Commands inside the exam container

```text
exam help|status|questions|submissions|finish

1511 fetch [ACTIVITY]
1511 autotest ACTIVITY [TEST_SELECTOR]
autotest ACTIVITY [TEST_SELECTOR]
submit ACTIVITY [FILE ...]
1511 check

1521 fetch PACK
1521 autotest ACTIVITY [TEST_SELECTOR]
1521 mipsy FILE [ARG ...]
submit ACTIVITY [FILE ...]
1521 check
1521 classrun -check
1521 classrun ACTIVITY

check
```

Autotest and submit are separate. Autotest shows each command and test result;
incorrect output includes actual output, expected output, a diff, input, and
reproduction commands. `passed` and an all-passing summary are green in a TTY.
`NO_COLOR` or redirected output is always plain text.

Questions may be addressed as `q1`, `q2`, and so on. A successful submission
prints one line: `Your answer (FILE) for q1 has been submitted.` The shared
`check` command and `1521 classrun -check` list the questions with accepted
submissions. `1521 classrun q1` prints the latest submitted source with its
filename, candidate, UTC submission time, and line numbers.

Ordinary commands come from Debian. `ls`, `ls -la`, `cd`, `cat`, `vim`, `nano`,
`make`, `gcc`, `clang`, `dcc`, `gdb`, and `valgrind` are available. `la` is a
personal shell alias rather than a standard command, so it is not defined.

## Resume, export, and report

```sh
.venv/bin/csetty attempts list
.venv/bin/csetty resume [ATTEMPT_ID]
.venv/bin/csetty code [ATTEMPT_ID]
.venv/bin/csetty page [ATTEMPT_ID]
.venv/bin/csetty export ATTEMPT_ID EMPTY_DESTINATION
.venv/bin/csetty report [ATTEMPT_ID]
.venv/bin/csetty report [ATTEMPT_ID] --json
```

Closing the shell or VS Code never pauses or finishes a timed attempt. A
persisted UTC deadline is reused after a restart. Final grading uses only the
latest accepted submission for each question, never unsaved or later workspace
content. At 60, 30, 15, and 5 minutes remaining, the supervisor broadcasts an
English warning to every open exam terminal, including VS Code integrated
terminals. Every report is prominently labelled as a local estimate.
After `exam finish` or automatic timed expiry, the supervisor grades the latest
accepted submissions, writes both report formats, and opens the HTML report in
the host's default browser. The companion redirects only after the grade and
both atomic report writes are durably marked complete, so an earlier working
report cannot be mistaken for the final result. If the browser cannot be
launched, the absolute report path remains in the terminal or supervisor log and `csetty report
[ATTEMPT_ID]` remains available. Without an ID, `report` selects the newest
attempt; every successful `start` also prints the full ID before reading begins.
Outside the initial reading transition, a browser-launch failure is nonfatal and
the ready loopback URL is printed so the timed workspace can still open.

## Original question banks

The source checkout contains 75 original questions for each course:

```sh
.venv/bin/csetty bank validate comp1511
.venv/bin/csetty bank stats comp1521
.venv/bin/csetty bank verify comp1521
.venv/bin/csetty bank build comp1511 /tmp/comp1511-paper --seed 1511
.venv/bin/csetty bank build comp1521 /tmp/comp1521-paper --seed 1521
```

Generation is deterministic for a given bank, seed, and version. COMP1511
builds an 11-question, 100-mark paper with array and linked-list hurdles.
COMP1521 builds a 10-question, 100-mark paper: Q1–4 foundations, Q5 Unicode,
Q6–8 advanced systems/MIPS/files, Q9 processes or threads, and Q10 a required
challenge combination. `bank verify` builds an author-only temporary pack and
runs every one of the selected course bank's 75 reference solutions against all
public and after-finish tests in the real isolated judge. See [question-bank
format and blueprints](docs/QUESTION_BANK.md).

## Important limitations

- Locally installed post-finish tests are withheld from the normal UI, not
  genuinely secret from the computer owner.
- Docker can block networking in exam containers, but cannot block another host
  application or another ordinary VS Code window.
- A local administrator, host-clock manipulation, and deliberate Docker/state
  tampering are outside the local alpha threat model.
- The simulator provides behavioural familiarity, not a byte-for-byte copy of
  a term-specific UNSW system.
- The author-only `solutions/` trees are excluded from pack digests and from
  every judge mount; they are never placed in a student workspace. They remain
  in host installation assets so a finished report can reveal the exact worked
  solution snapshotted when the attempt began.

## Documentation and public references

- [Command contract](docs/COMMAND_SPEC.md)
- [Pack schema](docs/PACK_FORMAT.md)
- [VS Code integration](docs/VSCODE_INTEGRATION.md)
- [Exam companion page](docs/COMPANION_PAGE.md)
- [Question-bank format and blueprints](docs/QUESTION_BANK.md)
- [Curriculum and assessment-shape sources](docs/CURRICULUM_SOURCES.md)
- [Implementation plan and release gates](docs/PROJECT_PLAN.md)
- [Release process and fail-closed gates](docs/RELEASING.md)
- [Release evidence for 0.1.0a1](docs/RELEASE_EVIDENCE_0.1.0a1.md)
- [File-level licence map](LICENSES.md)
- [Assessment materials licence](ASSESSMENT_MATERIALS_LICENSE.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
- [Trademarks and non-affiliation](TRADEMARKS.md)
- [UNSW exam rules](https://www.unsw.edu.au/student/managing-your-studies/academic-life/assessments-exams-resources/exams/rules)
- [Public COMP1511 practice exam](https://cgi.cse.unsw.edu.au/~cs1511/26T1/pracexam/index.html)
- [Public COMP1521 released practice exam](https://cgi.cse.unsw.edu.au/~cs1521/26T1/exam/22t3final/questions)
- [DCC repository](https://github.com/COMP1511UNSW/dcc)
- [mipsy repository](https://github.com/insou22/mipsy)

Public pages inform workflow and structure only. The bundled questions and
wording are original CSEExamTTY material.

## Licensing

The host software and build definitions are Apache-2.0. All original files in
`packs/**` and `question_bank/**`, including prose, starter code, tests, and
solutions, are CC BY-NC-ND 4.0. Third-party components keep their own licences.
See [the path-based licence map](LICENSES.md) before copying or redistributing
the package. No licence grants UNSW affiliation or project trademark rights.
