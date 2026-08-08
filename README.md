# CSEExamTTY

CSEExamTTY lets you practise COMP1511- and COMP1521-style programming exams on
your own computer. It gives you an isolated Linux workspace, course-like
commands, autotests, local submissions, timed exam mode, and a detailed report
with worked solutions after you finish.

> [!IMPORTANT]
> CSEExamTTY is alpha software. The latest public PyPI release is
> [`0.1.0a1`](https://pypi.org/project/cseexamtty/0.1.0a1/) and contains the
> earlier 150-question bank. This source checkout is the `0.1.0a3` release
> candidate and contains the expanded 300-question bank described below.

It is not made, managed, endorsed, or authenticated by UNSW or the UNSW School
of Computer Science and Engineering. It never connects to UNSW systems, and no
local submission is an official submission.

## Quick start

The normal workflow is:

`install` → `doctor` → `prepare` once → `start` → `autotest`/`submit` → `finish`

There are two different things you can start from:

- `comp1511-original-a` and `comp1521-original-a` are **fixed papers**. Each
  contains the same questions every time you start it.
- `comp1511` and `comp1521` are **150-question banks**. A bank is not a paper
  and cannot be started directly; first use `csetty bank build` to select a
  new 100-mark paper from it.

### 1. Install the prerequisites

You need:

- Python 3.11 or later;
- Docker Desktop or Docker Engine, running before you start; and
- VS Code with the `code` command available for preparation and the default
  editor workflow.

### 2. Install CSEExamTTY

For the latest published alpha:

```sh
pipx install cseexamtty==0.1.0a1
# or
uv tool install cseexamtty==0.1.0a1
```

To use the current source checkout instead:

```sh
git clone https://github.com/JiaruiUNSW/CSEtty.git
cd CSEtty
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, create the environment with `py -3.11 -m venv .venv`
and activate it with `.\.venv\Scripts\Activate.ps1`. The remaining `csetty`
commands are the same on every platform.

### 3. Prepare one course

Check the host, build the local course images, and confirm that the course is
ready for an offline attempt:

```sh
csetty doctor
csetty prepare --profile comp1511
csetty doctor --offline-ready comp1511
```

Preparation is a one-time networked step for each version of a course image. It
also opens a clearly labelled, isolated CSEExamTTY VS Code window while it
caches the required extensions. Use `--profile comp1521` for COMP1521 or
`--profile all` to prepare both courses.

### 4. Start a practice attempt

Practice mode is untimed by default:

```sh
csetty start comp1511-original-a
```

For COMP1521:

```sh
csetty start comp1521-original-a
```

CSEExamTTY opens the local paper and your isolated workspace. No work is sent
to UNSW or to any other marking system.

### 5. Solve, test, submit, and finish

Inside the exam terminal, open and edit the starter file named in the paper,
then run a workflow like this:

```text
exam questions
1511 autotest q1
submit q1
check
exam finish
```

Use `1521 autotest q1` in a COMP1521 attempt. `submit` is separate from
`autotest`: only submitted files are graded. After you confirm `exam finish`,
CSEExamTTY grades the latest accepted submission for each question and opens
the local HTML report.

## Choose your next action

| I want to... | Run... |
| --- | --- |
| See the installed fixed papers | `csetty packs list` |
| Practise COMP1511 without a timer | `csetty start comp1511-original-a` |
| Practise COMP1521 without a timer | `csetty start comp1521-original-a` |
| Run the full timed simulation | `csetty start comp1511-original-a --mode exam` |
| Work only in the terminal | add `--editor terminal` to `csetty start` |
| Continue the newest active attempt | `csetty resume` |
| Reopen the paper or workspace | `csetty page` or `csetty code` |
| Reopen the latest report | `csetty report` |
| Generate and sit a different timed paper | follow [Build and sit a random exam paper](#build-and-sit-a-random-exam-paper) |

Run `csetty --help` or `csetty COMMAND --help` whenever you need the full list
of options.

## What is included

The current source checkout includes:

- a fixed 11-question, 100-point COMP1511 paper covering C, arrays, linked
  lists, debugging, functions, and whole programs;
- a fixed 10-question, 100-point COMP1521 paper covering C, MIPS, file I/O,
  Unicode, processes, pipes, and threads;
- two 150-question banks (300 original questions total), with difficulty 1–5,
  topic/week tags, worked solutions, reference programs, and at least five test
  points for every question;
- random paper generation that covers every declared topic and orders questions
  from easier to harder;
- untimed practice and a full simulation with 10 minutes of reading time and
  180 minutes of working time;
- course-like fetch, autotest, submit, check, classrun, DCC, and MIPS commands in
  an isolated Linux workspace with networking disabled by default; and
- immutable local submissions plus HTML, text, and JSON reports with test
  evidence, submitted code, worked solutions, strengths, gaps, and revision
  advice.

## One-time preparation

Preparation is the only phase that may download or build tooling:

```sh
csetty prepare --profile comp1511
csetty prepare --profile comp1521
```

Each preparation uses the digest-pinned Debian 12 multi-architecture base,
downloads the SHA-256-pinned DCC 2.37 source archive and runs its upstream
`make dcc` build locally. It stages the installed external `csetty-mips` source
at its pinned Git commit for COMP1521. No DCC binary, prebuilt course image,
registry layer, public BuildKit cache, VS Code Server, or VSIX cache is shipped
by this repository. `start` verifies the recorded interactive and judge image
IDs and never builds or pulls an image.

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

## Practice and exam modes

| Mode | What happens | Example |
| --- | --- | --- |
| Practice (default) | No timer and no simulated sign-in | `csetty start comp1511-original-a` |
| Exam | 10 minutes reading, 180 minutes working, timed and offline | `csetty start comp1511-original-a --mode exam` |

Add `--editor terminal` if you prefer a terminal instead of VS Code.

Exam mode starts in the host terminal. CSEExamTTY clears that terminal, asks
for a simulated zID and password, shows the local-system warning, and requires
you to type `yes`. The password is never authenticated, stored, hashed, or
logged. **Do not enter a real UNSW password.**

During reading time, the browser shows the complete read-only paper but no
editable workspace. When reading ends, CSEExamTTY opens the starter workspace
and editor. The paper remains available beside the editor with the current
state and countdown.

The paper is served only from `127.0.0.1` using an unguessable local path. Its
**Open VSC** button reconnects to the same attempt without resetting the clock.
If a browser or editor window is closed, use `csetty page`, `csetty code`, or
`csetty resume` to reopen it.

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
csetty attempts list
csetty resume [ATTEMPT_ID]
csetty code [ATTEMPT_ID]
csetty page [ATTEMPT_ID]
csetty export ATTEMPT_ID EMPTY_DESTINATION
csetty report [ATTEMPT_ID]
csetty report [ATTEMPT_ID] --json
```

The attempt ID is printed by `start`. When an optional ID is omitted, `resume`,
`code`, `page`, and `report` select the newest relevant attempt.

Closing the terminal or VS Code does not pause or finish a timed attempt. Its
saved deadline continues to run. Final grading uses the latest accepted
submission for each question, not unsaved editor content. After `exam finish`
or timed expiry, the HTML report normally opens automatically; use
`csetty report` if it does not. Every score is labelled as a local estimate.

## Build and sit a random exam paper

`comp1511-original-a` is one fixed paper. By contrast, `comp1511` names the
150-question COMP1511 bank used by the generator. The same distinction applies
to `comp1521-original-a` and the `comp1521` bank. A generated paper selects 11
COMP1511 questions or 10 COMP1521 questions; it does not place all 150 bank
questions into one exam.

Choose an integer seed and a new destination directory, then start the generated
directory in exam mode:

```sh
csetty bank build comp1511 ./comp1511-paper-1511 --seed 1511
csetty start ./comp1511-paper-1511 --mode exam
```

For COMP1521:

```sh
csetty bank build comp1521 ./comp1521-paper-1521 --seed 1521
csetty start ./comp1521-paper-1521 --mode exam
```

Do not omit `--mode exam` when you want the normal exam workflow. CSEExamTTY
shows the Welcome screen, asks for the simulated zID and password, displays the
exam-condition acknowledgement, opens the complete paper for the read-only
reading period, and only then creates the starter workspace for working time.

Generated starter and submission filenames follow their position in the paper:
`q1.c`, `q2.c`, and so on. A COMP1521 MIPS question uses the corresponding
`.s` name, such as `q3.s`. Use `exam questions`, `1511 autotest q1` or
`1521 autotest q1`, and `submit q1` just as you would in a fixed paper.

Use a different seed for a different paper. Reusing the same bank version and
seed produces the same paper. Every generated paper covers all declared course
topic tags and becomes progressively harder from its first question to its
last.

Authors can inspect or verify a bank with:

```sh
csetty bank stats comp1511
csetty bank validate comp1511
csetty bank verify comp1511
```

`bank verify` runs all 150 reference solutions for that course against every
public and post-finish test in the isolated judge. See the
[question-bank format and blueprints](docs/QUESTION_BANK.md) for the authoring
contract.

## Troubleshooting

Start with these two checks:

```sh
csetty doctor
csetty doctor --offline-ready comp1511
```

| If you see... | Do this... |
| --- | --- |
| `Docker daemon: FAIL` | Start Docker Desktop or the Docker service, then rerun `csetty doctor`. |
| `VS Code CLI: FAIL` | Install VS Code's `code` command in your shell path. |
| `Local images` or `Offline VS Code` fails | Rerun `csetty prepare --profile comp1511`. |
| The paper or editor was closed | Run `csetty page`, `csetty code`, or `csetty resume`. |
| The final report did not open | Run `csetty report` and use the printed local path. |

If the problem remains, include the output of `csetty doctor`, your operating
system, Python version, Docker version, and CSEExamTTY version in a
[GitHub issue](https://github.com/JiaruiUNSW/CSEtty/issues).

## COMP1521 MIPS support

Installing CSEExamTTY also installs the independently implemented
[`csetty-mips==0.1.1`](https://pypi.org/project/csetty-mips/0.1.1/) teaching
engine used by the COMP1521 image. No upstream mipsy source or binary is
included. See the [integration note](docs/CSETTY_MIPS_INTEGRATION.md) and the
[CSEtty-MIPS repository](https://github.com/JiaruiUNSW/CSEtty-MIPS) for its CLI,
Python API, specification, and provenance.

## Project status

This repository is the `0.1.0a3` source-only alpha release candidate. The latest
published PyPI alpha is `0.1.0a1`. The current course images have passed the
complete prepare, attach, companion, autotest, submit, finish, judge, and report
workflow on the current Apple Silicon development Mac. Exact commit
`bc9d47bb65ee246e488d3a14156c0965e530c754` also passed the recorded native
Windows acceptance run described in
[`docs/WINDOWS_VALIDATION_RESULTS_0.1.0a3.md`](docs/WINDOWS_VALIDATION_RESULTS_0.1.0a3.md).

The repository publishes source and original assessment materials, not course
images, DCC binaries, Docker layers, VS Code Server files, or extension caches.
`csetty prepare` builds and records those local assets explicitly. A future
stable release still requires broader native desktop and offline VS Code
acceptance across additional hosts.

## Development

For an editable development environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/ruff check src tests scripts
.venv/bin/mypy src/csetty
.venv/bin/pytest -q
```

You can use `uv sync --extra dev` instead when `uv` is installed. On Windows,
replace `.venv/bin/` with `.venv\Scripts\`.

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
