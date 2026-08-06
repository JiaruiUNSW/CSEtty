# Exam companion page

Status: implemented for working, finished, and expired attempts.

## Lifecycle

During formal exam mode, sign-in, acknowledgement, and reading time remain in
the host terminal. No editable container exists during reading time. When the
working period begins, CSEExamTTY starts the supervised interactive container,
opens the isolated VS Code profile, and opens the companion page in the default
browser.

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
- detailed links for every question;
- bundled offline resources declared by the pack;
- an index of relevant official public course pages; and
- an **Open VSC** recovery control.

Each question page renders the pack's original Markdown prompt, including
background, exact requirements, examples, implementation notes, required
filename, marks, difficulty, track, and tags.

Official course links are not mirrored content. They open in the host browser
and remain usable during an exam whenever the host has network access because
`--network none` applies to Docker, not the host. They are clearly separated
from bundled offline resources, and Docker's network policy never claims to
control the host browser.

## Open VSC recovery

The button issues a same-origin POST to the local service. The service verifies
that the attempt is still working and that the isolated profile is fully cached,
starts the existing container only if it is stopped, ensures the same
supervisor is running, and attaches VS Code to the existing container URI. It
does not create a new attempt, replace the workspace, or extend the deadline.

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
