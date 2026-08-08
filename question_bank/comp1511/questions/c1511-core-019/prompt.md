# Repair the Range Clamp

## Background

The supplied program is intended to clamp a value to an inclusive interval, but its branch order and returned bounds are wrong.

## Requirements

Write or repair the complete C program in `c1511_core_019.c`.

**Input:** One line contains lower, upper, and value, where lower <= upper.

**Output:** Print `clamped: x`, using lower when value is below the interval, upper when it is above, and value otherwise.

**Assumptions:** All three numbers fit in a C `int`.

**Restrictions:** Repair the supplied `clamp` function. Keep the input and output interface unchanged and do not replace the result with test-specific constants.

Submit exactly the file `c1511_core_019.c`.

## Examples

Input:

```text
0 10 14
```

Output:

```text
clamped: 10
```

Fourteen is above the interval, so it is clamped to the upper bound.

## Implementation notes

Each out-of-range comparison must return the boundary on that same side. Output spelling, spaces, punctuation, and newlines must match exactly.
