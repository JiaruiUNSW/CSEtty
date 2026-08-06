# Clamp and count

## Background

This original short exercise isolates one core C skill behind a complete command-line harness. `size_t clamp_values(int *values, size_t length, int low, int high)` clamps every value to the inclusive interval and returns how many elements changed. Inputs are supplied as documented so the target behaviour can be reproduced directly.

## Requirements

- The first two command-line arguments are valid bounds with `low <= high`; remaining arguments are values.
- Values already on either boundary do not count as changed.
- Print the change count on one line and the resulting array on the next.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

`./c1511_adv_018 0 10 -2 5 12` prints `changes=2` followed by `0 5 10`.

## Implementation notes

Modify values in place. The provided output helper prints `EMPTY` for zero values. Submit `c1511_adv_018.c`. Keep all provided function signatures and harness code unless the task explicitly identifies a starter bug. Build and submit the unique source file using the shell-free `dcc -Werror` command supplied by the pack.
