# Order the endpoint values

## Background

This original short exercise isolates one core C skill behind a complete command-line harness. `void order_endpoints(int *first, int *last)` swaps the values addressed by its two pointers only when the first value is greater than the last. Inputs are supplied as documented so the target behaviour can be reproduced directly.

## Requirements

- For arrays of fewer than two values, the harness does not call the function.
- Do not reorder any interior element.
- Perform the swap through the pointers without indexing the array inside the function.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

`./c1511_adv_017 9 2 4` prints `4 2 9`; `1 5` remains `1 5`.

## Implementation notes

The command-line arguments are the array values. The harness allocates, prints, and frees the array. Submit `c1511_adv_017.c`. Keep all provided function signatures and harness code unless the task explicitly identifies a starter bug. Build and submit the unique source file using the shell-free `dcc -Werror` command supplied by the pack.
