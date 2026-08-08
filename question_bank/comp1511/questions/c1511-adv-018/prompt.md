# Clamp and count

## Background

`size_t clamp_values(int *values, size_t length, int low, int high)` clamps every value to the inclusive interval and returns how many elements changed.

## Requirements

- The first two command-line arguments are valid bounds with `low <= high`; remaining arguments are values.
- Values already on either boundary do not count as changed.
- Print the change count on one line and the resulting array on the next.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_018 0 10 -2 5 12
```

Output:

```text
changes=2
0 5 10
```

## Implementation notes

Modify values in place. The provided output helper prints `EMPTY` for zero values. Submit `c1511_adv_018.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
