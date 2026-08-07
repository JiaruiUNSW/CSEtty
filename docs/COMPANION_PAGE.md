# Exam companion page

Status: implemented for reading, working, finished, and expired attempts.

## Lifecycle

During formal exam mode, sign-in and acknowledgement remain in the host
terminal. Before reading time begins, CSEExamTTY starts the companion, waits for
its loopback endpoint to become healthy, and asks the default browser to open
the full read-only paper. Only after that browser-launch call succeeds does it
persist the reading start time. The page exposes every question prompt and the
pack's explicitly permitted local resources, but it does not create an editable
workspace or container and does not offer an editor control. A failed launch
leaves the attempt in resumable `CREATED`
state without deducting reading time. In `CREATED`, the companion exposes only a
waiting page and rejects all question and resource routes, so its recovery URL
cannot reveal the paper before the clock starts. When the
working period begins, the page automatically refreshes to working state while
CSEExamTTY starts the supervised interactive container and opens the isolated
VS Code profile. On explicit finish or timed expiry, the supervisor generates
the final reports, keeps the companion service alive as an authenticated report
viewer, and redirects the existing browser page to the final report. CSEExamTTY
also asks the host to open that HTTP report URL, with the generated local HTML
file retained as a fallback when the companion is unavailable.
The redirect and **Open final report** control remain pending until a persisted
finalization marker confirms the grade plus JSON and HTML writes completed; an
HTML report generated while working is never treated as final.
All report publishers for an attempt share a cross-process lock. A rewrite
withdraws that marker before replacing either file and republishes it only after
both replacements succeed, so a concurrent working report cannot overwrite a
finished report while it remains advertised as final.

The page can be reopened without changing the attempt:

```text
csetty page [ATTEMPT_ID]
```

`csetty resume` also reuses the live page process when possible. A companion
process is scoped to one attempt and reads current attempt/submission state from
SQLite on each request.

## Student interface

The overview contains:

- local-simulation and non-UNSW notice;
- attempt state, persisted deadline, and live countdown;
- question order, marks, track, tags, and latest submission sequence;
- every complete question prompt in one long-form paper plus focused links;
- bundled offline resources declared by the pack;
- an index of relevant official public course pages outside reading time; and
- an **Open VSC** recovery control while the attempt is working; and
- an **Open final report** control only after the persisted finalization marker
  confirms grading and both JSON/HTML report writes completed.

Each question page renders the pack's original Markdown prompt, including
background, exact requirements, examples, implementation notes, required
filename, marks, difficulty, track, and tags.

## Visual contract

The companion and final HTML report use one packaged, offline theme. It follows
the common public COMP1511/COMP1521 exam-page vocabulary without importing
remote Bootstrap, course CSS, logos, or scripts: course-colour navigation, a
light examination jumbotron, bordered section headings with a left colour tab,
Bootstrap-style cards/alerts/tables, and light code or terminal blocks.

The profile selects only the established course variant:

- COMP1511: green accent `#6abd6e`, wide exam column;
- COMP1521: teal accent `#42a097`, narrower exam column.

The shared CSS is emitted from `src/csetty/web_theme.py` into both surfaces and
is identified by `data-csetty-theme="cse-course-exam-v1"`. Page-specific CSS may
only cover live controls or report results; it must not redefine the course
shell. This keeps reading, working, finished companion views and the generated
report visually consistent.

Official course links are not mirrored content. They open in the host browser
and remain usable during an exam whenever the host has network access because
`--network none` applies to Docker, not the host. They are clearly separated
from bundled offline resources, and Docker's network policy never claims to
control the host browser. They are hidden during reading time so that the page
shows only resources explicitly permitted by the paper.

## Open VSC recovery

The **Open VSC** button issues a same-origin POST to the local service. The
service verifies that the attempt is still working and that the isolated profile
is fully cached, starts the existing container only if it is stopped, ensures
the same supervisor is running, and attaches VS Code to the existing container
URI. It does not create a new attempt, replace the workspace, or extend the
deadline.

Requests are rate-limited. Errors are returned on the page rather than silently
falling back to a normal VS Code profile or terminal.

## Local security boundary

- The HTTP listener binds only to `127.0.0.1` on an ephemeral port.
- Every URL contains a random token and responses use `Cache-Control: no-store`.
- POST origin, path, method, and request size are checked.
- Markdown is rendered through an escaping allowlist; raw HTML is not trusted.
- CSP, frame denial, no-sniff, and no-referrer headers are sent.
- The page executes no shell command and never accepts arbitrary container,
  folder, executable, or Docker arguments.

This protects against accidental cross-origin actions and local path injection;
it is not intended to defend against the computer owner or a local
administrator.
