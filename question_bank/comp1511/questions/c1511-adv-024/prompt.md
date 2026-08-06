# Append a dynamic checksum

## Background

This original short exercise isolates one core C skill behind a complete command-line harness. `int append_checksum(int **values, size_t *length)` grows a heap array by one element containing the sum of all original elements. Inputs are supplied as documented so the target behaviour can be reproduced directly.

## Requirements

- For an empty array, append the checksum zero.
- Update both caller-owned outputs only after successful `realloc`; return 1 on success and 0 on allocation failure.
- The harness prints the grown array and frees the final pointer.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

`./c1511_adv_024 1 2 3` prints `1 2 3 6`; no input values print `0`.

## Implementation notes

Assume the checksum and allocation-size calculation fit their types. Use a temporary pointer for `realloc`. Submit `c1511_adv_024.c`. Keep all provided function signatures and harness code unless the task explicitly identifies a starter bug. Build and submit the unique source file using the shell-free `dcc -Werror` command supplied by the pack.
