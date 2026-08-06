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
- Uses DCC's supported Valgrind runtime automatically on Docker Desktop WSL2,
  where independently compiled ASan binaries can terminate nondeterministically.

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
