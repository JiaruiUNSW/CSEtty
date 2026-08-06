# Changelog

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

