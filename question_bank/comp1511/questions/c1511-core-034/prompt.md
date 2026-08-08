# Busiest Two-by-Two Window

## Background

A rectangular activity map is inspected through every possible two-by-two window. The busiest window has the greatest sum; ties go to the smallest top row, then smallest left column.

## Requirements

Write a complete C program in `c1511_core_034.c`.

**Input:** The first line contains rows and columns (2 <= rows, columns <= 20), followed by integer activity values.

**Output:** Print `top: r c` for the zero-based top-left coordinate and `sum: s`.

**Assumptions:** All window sums fit in a C `int`; values may be negative.

**Restrictions:** Store the map in a two-dimensional array and use a helper to calculate a window sum.

Submit exactly the file `c1511_core_034.c`.

## Examples

Input:

```text
3 3
1 2 0
0 4 1
2 0 3
```

Output:

```text
top: 1 1
sum: 8
```

The bottom-right window contains 4, 1, 0, and 3, whose sum eight is largest.

## Implementation notes

Initialise the best from window (0, 0), because zero is not a safe initial sum for negative grids. Match every required label, space, punctuation mark, and newline exactly.
