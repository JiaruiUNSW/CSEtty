# Strictly Rising Columns

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A column in a measurement table is rising when every value below the first is strictly greater than the value directly above it.

## Requirements

Write a complete C program in `c1511_core_009.c`.

**Input:** The first line contains rows and columns (1 <= rows, columns <= 20), followed by the integer table.

**Output:** Print `rising columns: k`.

**Assumptions:** A one-row column is rising because it contains no violating adjacent pair.

**Restrictions:** Use a two-dimensional array and a helper that decides one column. Do not sort.

Submit exactly the file `c1511_core_009.c`.

## Examples

Input:

```text
3 3
1 3 0
2 2 1
3 4 1
```

Output:

```text
rising columns: 1
```

Only the first column increases strictly at each step.

## Implementation notes

The first non-increasing adjacent pair is enough to reject a column. Your output must match the specified spelling, spacing, and newlines exactly.

