# Matrix Border Sum — solution guide

## Approach

Store the matrix, then use nested row and column loops. Add a cell when its row is zero or `rows-1`, or its column is zero or `cols-1`.

## Correctness

The condition is true exactly for cells on at least one of the four boundaries. Each cell is visited once, so corners and degenerate dimensions are included once rather than once per matching edge.

## Complexity

O(rows*cols) time and O(rows*cols) input storage, with O(1) stack space.

## Common pitfalls

Summing four edges independently double-counts corners and badly mishandles one-row matrices. Compute byte offsets as `(row*cols+col)*4`.
