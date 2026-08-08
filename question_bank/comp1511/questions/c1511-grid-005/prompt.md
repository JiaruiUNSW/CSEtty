# Four-Neighbour Terrain Peaks

## Background

A rectangular grid models a spatial survey. Rows and columns may differ, so every index calculation must use the supplied column count.

## Requirements

Read `rows columns` (each 0 to 8), then the grid in row-major order. Compute the metric in the title and print `result: X`.

**Exact rule.** Count cells strictly greater than every existing orthogonal neighbour; a neighbourless cell does not count.

Submit `c1511_grid_005.c`. Your program must not print prompts or explanatory text.

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
result: 1
```

## Implementation notes

Store the grid in a bounded flat or two-dimensional array. Check dimensions before accessing the first cell or a neighbour/window.
