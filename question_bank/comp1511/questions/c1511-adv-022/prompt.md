# Find the first signed decimal

## Background

This original short exercise isolates one core C skill behind a complete command-line harness. `int first_decimal(const char *text, int *value)` finds the first decimal integer token and stores it through `value`, returning 1 on success and 0 otherwise. Inputs are supplied as documented so the target behaviour can be reproduced directly.

## Requirements

- A token is digits optionally preceded immediately by `+` or `-`; a sign not followed by a digit is skipped.
- Search resumes after invalid characters, and stop after the first valid token.
- Assume a found integer fits in `int`; do not call `atoi`, `strtol`, or `sscanf`.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

`./c1511_adv_022 'abc -42x'` prints `-42`; `./c1511_adv_022 none` prints `NONE`.

## Implementation notes

Exactly one text argument is supplied. Cast to `unsigned char` before passing bytes to `isdigit`. Submit `c1511_adv_022.c`. Keep all provided function signatures and harness code unless the task explicitly identifies a starter bug. Build and submit the unique source file using the shell-free `dcc -Werror` command supplied by the pack.
