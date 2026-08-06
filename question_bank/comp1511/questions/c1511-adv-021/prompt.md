# Distance between first extremes

## Background

This original short exercise isolates one core C skill behind a complete command-line harness. `size_t first_extreme_distance(const int *values, size_t length)` returns the index distance between the first minimum and first maximum. Inputs are supplied as documented so the target behaviour can be reproduced directly.

## Requirements

- For zero or one value, return zero.
- When a minimum or maximum occurs repeatedly, use its first occurrence.
- Return the nonnegative absolute difference between their zero-based indices.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

`./c1511_adv_021 4 1 7 1 7` prints `1`, because the first minimum is index 1 and first maximum is index 2.

## Implementation notes

Use strict comparisons so ties retain their earlier indices. The input array is read-only. Submit `c1511_adv_021.c`. Keep all provided function signatures and harness code unless the task explicitly identifies a starter bug. Build and submit the unique source file using the shell-free `dcc -Werror` command supplied by the pack.
