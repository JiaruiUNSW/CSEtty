# Repair running differences

## Background

This original short exercise isolates one core C skill behind a complete command-line harness. `void running_differences(int *values, size_t length)` must keep element zero and replace every later element with its original value minus the original preceding value. Inputs are supplied as documented so the target behaviour can be reproduced directly.

## Requirements

- Perform the transformation in place.
- The calculation for an index must use the predecessor's original value, not its already transformed value.
- Empty and one-element arrays are unchanged.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

`./c1511_adv_019 5 9 12` must print `5 4 3`. The starter's loop produces the wrong last difference.

## Implementation notes

Diagnose and repair only the marked function. Saving the previous original value is sufficient; a second array is unnecessary. Submit `c1511_adv_019.c`. Keep all provided function signatures and harness code unless the task explicitly identifies a starter bug. Build and submit the unique source file using the shell-free `dcc -Werror` command supplied by the pack.
