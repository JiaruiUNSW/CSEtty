# Calm Grid Rows

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A monitoring grid records several readings per station row. A row is calm when the difference between its largest and smallest readings does not exceed a supplied tolerance.

## Requirements

Write a complete C program in `c1511_core_005.c`.

**Input:** The first line contains rows, columns, and tolerance (1 <= rows, columns <= 20; tolerance >= 0), followed by rows lines of integer grid values.

**Output:** Print `calm rows: k`.

**Assumptions:** All values and row ranges fit in a C `int`.

**Restrictions:** Store the grid in a two-dimensional array and use a helper to compute a row range.

Submit exactly the file `c1511_core_005.c`.

## Examples

Input:

```text
2 3 2
1 2 3
5 8 6
```

Output:

```text
calm rows: 1
```

The first row has range 2; the second has range 3.

## Implementation notes

Initialise both the minimum and maximum from the first element of a row rather than from zero. Your output must match the specified spelling, spacing, and newlines exactly.

