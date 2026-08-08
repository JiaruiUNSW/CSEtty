# Coastal Grid Border Total

## Task

Sum cells in the first/last row or first/last column exactly once; empty grids return 0.

## Background

A rectangular grid models a spatial survey. Rows and columns may differ, so every index calculation must use the supplied column count.

## Requirements

Read `rows columns` (each 0 to 8), then the grid in row-major order. Print the computed value as `result: X` followed by one newline.

## Starter code

Complete `static long long solve(const int *a, int rows, int columns)`. The grid is stored in row-major order, so cell `(r, c)` is `a[r * columns + c]`.

## Examples

Input:

```text
2 3
1 2 3
4 5 6
```

Output:

```text
result: 21
```

## Implementation notes

Store the grid in a bounded flat or two-dimensional array. Check dimensions before accessing the first cell or a neighbour/window.

## Submission

Submit `c1511_grid_001.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
