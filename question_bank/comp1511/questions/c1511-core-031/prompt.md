# Row Champion

## Background

Rows in a score grid compete using two measures. Higher row sum wins; when sums tie, the row with the smaller range (maximum minus minimum) wins; a remaining tie goes to the lower row index.

## Requirements

Write a complete C program in `c1511_core_031.c`.

**Input:** The first line contains rows and columns (1 <= rows, columns <= 20), followed by the integer grid.

**Output:** Print the winning zero-based row as `row: r`, then its `sum: s` and `range: d`.

**Assumptions:** All row sums and ranges fit in a C `int`.

**Restrictions:** Store the grid in a two-dimensional array and use a helper to compute both statistics for one row.

Submit exactly the file `c1511_core_031.c`.

## Examples

Input:

```text
3 3
1 2 3
4 0 2
-1 10 -1
```

Output:

```text
row: 2
sum: 8
range: 11
```

The third row has the greatest sum, so its larger range does not matter.

## Implementation notes

Initialise the champion from row zero, especially because every possible sum may be negative. Match every required label, space, punctuation mark, and newline exactly.
