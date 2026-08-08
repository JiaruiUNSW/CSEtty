# Coastal Grid Border Total

## Background

A rectangular grid models a spatial survey. Rows and columns may differ, so every index calculation must use the supplied column count.

## Requirements

Read `rows columns` (each 0 to 8), then the grid in row-major order. Compute the metric in the title and print `result: X`.

**Exact rule.** Sum cells in the first/last row or first/last column exactly once; empty grids return 0.

Submit `c1511_grid_001.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

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
