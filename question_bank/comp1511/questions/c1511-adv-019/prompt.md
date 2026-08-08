# Repair running differences

## Background

`void running_differences(int *values, size_t length)` must keep element zero and replace every later element with its original value minus the original preceding value.

## Requirements

- Perform the transformation in place.
- The calculation for an index must use the predecessor's original value, not its already transformed value.
- Empty and one-element arrays are unchanged.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_019 5 9 12
```

Output:

```text
5 4 3
```

## Implementation notes

Diagnose and repair only the marked function. Saving the previous original value is sufficient; a second array is unnecessary. Submit `c1511_adv_019.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
