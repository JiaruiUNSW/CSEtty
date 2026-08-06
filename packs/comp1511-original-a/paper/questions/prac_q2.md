# Q2 — Sum the border of a square array

## Background

An image tile is represented by a square integer grid. Its border consists of the first and last rows together with the first and last columns.

## Requirements

Complete `border_sum` in `prac_q2.c`. Return the sum of every border cell exactly once. Interior cells must not contribute. The side length is between `1` and `MAX_SIZE` inclusive; values and the final sum fit in an `int`. Do not read input or print from inside `border_sum`, and do not modify the grid.

The supplied `main` reads the side length followed by `size * size` integers and prints one integer followed by a newline.

## Examples

```text
2
1 2
3 4
```

produces `10`. A three-by-three grid containing the values 1 through 9 row by row produces `40`. For a one-by-one grid, the only element is counted once.

## Implementation notes

A cell is on the border when its row or column is at an extreme index. A nested traversal makes the one-cell and two-cell cases natural and avoids double-counting corners. Submit only `prac_q2.c`.

