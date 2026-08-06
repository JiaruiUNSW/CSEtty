# Unique Column Beacons

This is an original C programming task for the local CSEExamTTY simulator.

## Background

Each column of a grid is a radio channel. A channel has a unique beacon when its maximum reading appears in exactly one row.

## Requirements

Write a complete C program in `c1511_core_006.c`.

**Input:** The first line contains rows and columns (1 <= rows, columns <= 20), followed by the integer grid.

**Output:** Print `unique beacons: k`, the number of columns with exactly one maximum.

**Assumptions:** Every grid value fits in a C `int`.

**Restrictions:** Use a two-dimensional array. Do not sort or copy columns into another array.

Submit exactly the file `c1511_core_006.c`.

## Examples

Input:

```text
3 3
1 5 2
4 5 3
0 2 3
```

Output:

```text
unique beacons: 1
```

Only column zero has a maximum that occurs once.

## Implementation notes

For each column, update both a current maximum and its occurrence count. A new maximum resets the count to one. Your output must match the specified spelling, spacing, and newlines exactly.

