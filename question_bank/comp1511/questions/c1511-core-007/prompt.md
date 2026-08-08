# Warm Cross Centres

## Background

For an interior grid cell, its cross neighbours are the cells immediately above, below, left, and right. A cell is warm when four times its value is greater than the sum of those neighbours.

## Requirements

Write a complete C program in `c1511_core_007.c`.

**Input:** The first line contains rows and columns (3 <= rows, columns <= 20), followed by the integer grid.

**Output:** Print `warm centres: k`.

**Assumptions:** The products and sums used by the comparison fit in a C `int`.

**Restrictions:** Use integer arithmetic only and ignore all border cells.

Submit exactly the file `c1511_core_007.c`.

## Examples

Input:

```text
3 3
0 0 0
0 5 0
0 0 0
```

Output:

```text
warm centres: 1
```

The centre contributes 20 on the left side of the comparison and its neighbours sum to zero.

## Implementation notes

Multiplying the centre by four compares it with the neighbour average without floating point. Your output must match the specified spelling, spacing, and newlines exactly.
