# Q4 — Count orthogonal peaks in a grid

## Background

A terrain cell is an orthogonal peak when it is strictly greater than the cells immediately above, below, left, and right of it.

## Requirements

Complete `count_peaks` in `prac_q4.c`. Count only interior cells, because border cells do not have four orthogonal neighbours. Diagonal cells are irrelevant. Equality with any neighbour means the cell is not a peak. Do not modify the grid and do not perform I/O inside the function.

The supplied program reads `rows cols`, then the grid values, and prints the count. Dimensions are positive and at most `MAX`; all values fit in `int`. A grid with fewer than three rows or columns has no eligible cells.

## Examples

```text
3 3
1 2 1
2 9 2
1 2 1
```

prints `1`. In a flat grid the answer is `0`.

## Implementation notes

Choose loop bounds that make every neighbour access valid without special cases inside the loop. Store the current value if that makes the four strict comparisons clearer. Submit `prac_q4.c`.

