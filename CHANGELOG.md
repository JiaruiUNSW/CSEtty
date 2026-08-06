# Changelog

## Unreleased

- Prepares the `0.1.0a3` source-only alpha release candidate while leaving its
  owner approval and new CI evidence fail-closed until they are completed.
- Clears the invoking terminal and scrollback before the simulated exam sign-in,
  then opens the full read-only paper in the browser during reading time.
- Uses one packaged COMP1511/COMP1521 course-exam theme for both the live paper
  and final report, with the appropriate green or teal course accent.
- Generates and opens the HTML report automatically after explicit finish or
  timed expiry, while retaining the durable report path if browser launch fails.
- Adds a protected, tokenless PyPI Trusted Publishing workflow triggered only
  by a published GitHub Release. The isolated OIDC job downloads no source and
  publishes only tag-matched, checksum-verified wheel/sdist assets.
- Restricts release checksums to the public wheel, sdist, and Python SBOM so the
  local DCC corresponding-source verification copy cannot become a release
  asset accidentally.
- Keeps Linux build entrypoints LF-only in Windows Git checkouts, tolerates slow
  companion/supervisor cold starts, and serves final reports through the
  authenticated loopback companion instead of Windows HTML file associations.
- Preserves question-bank and pack test fixtures byte-for-byte when Windows Git
  uses `core.autocrlf=true`, including printable fixtures with a `.bin` suffix.
- Enables Windows virtual-terminal processing before clearing the exam shell,
  starts reading time only after the companion is healthy and the browser launch
  succeeds, preserves resumable reading after launch failure, and lets `report`
  select the newest attempt when no attempt ID is supplied.
- Uses DCC's supported Valgrind runtime automatically on Docker Desktop WSL2,
  where independently compiled ASan binaries can terminate nondeterministically.
- Keeps a browser-launch failure nonfatal after reading has already started,
  persists the practice `--skip-reading` choice across `CREATED` recovery, and
  withholds every question and resource while a launch is still `CREATED`.
- Publishes companion report readiness only after the final grade and both
  durable report files have completed, preventing a pre-finish report from
  being redirected as the final result.
- Serializes report publication per attempt across processes and withdraws the
  finalization marker during every rewrite, so a concurrent working-time
  `csetty report` cannot overwrite or expose a stale final report.
- Stops an expired attempt's container even when resume-time report generation
  fails, terminates a companion child that misses its startup deadline, and
  contains permission races in the judge's direct-kill fallback.
- Uses a non-signalling Windows process-handle probe for companion and
  supervisor liveness, avoiding the terminating semantics of `os.kill(pid, 0)`
  on Windows.
- Accepts the live supervisor interpreter PID published by a Windows virtual
  environment instead of requiring it to match the redirector wrapper PID.
- Keeps companion referrers same-origin so the browser's **Open VSC** form POST
  retains its loopback origin without exposing tokenized paths to external sites.
- Rejects report publication while an attempt is still `CREATED`, closing the
  pre-reading report path, and bounds the interactive report-lock wait.

## 0.1.0a1 — 2026-08-06

First source-only public alpha.

- Implements timed local COMP1511/COMP1521-style attempts, immutable submission
  history, isolated judge execution, weighted reports, and exam-entry flow.
- Includes two original fixed practice papers and two original 75-question
  banks, with public/after-finish tests and worked solutions.
- Adds the isolated VS Code/companion-page workflow and terminal deadline
  broadcasts at 60, 30, 15, and 5 minutes.
- Uses the independent MPL-2.0 `csetty-mips 0.1.1` dependency for COMP1521.
- Publishes only source/build definitions and Python wheel/sdist. Course images,
  DCC binaries, Docker layers/caches, Debian archives, VS Code Server/VSIX
  caches, and upstream mipsy content are not release artifacts.
- Establishes the Apache-2.0 software and CC BY-NC-ND 4.0 assessment-material
  file-level licence map.

Known alpha limitation: full offline VS Code and Docker Desktop/WSL2 acceptance
has only been completed locally on Apple Silicon. Public CI covers the host
contract across Windows/Linux/macOS plus native Linux amd64/arm64 container
acceptance; broader desktop acceptance remains a stable-release gate.
