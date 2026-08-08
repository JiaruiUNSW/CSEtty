# Matrix Border Sum

## Background

Read `rows`, `cols`, then a row-major matrix. Call `border_sum(base, rows, cols)` and print the sum of entries in the outer border, counting every cell once.

## Requirements

The function must identify first/last rows or first/last columns. A one-row or one-column matrix must not double-count cells.

Input constraints: 1 <= rows,cols <= 4; the sum fits signed 32 bits.

Write your complete answer in `c1521_low_027.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
3
3
1
2
3
4
5
6
7
8
9
```

the exact output is:

```text
40
```

## Implementation notes

A single row-major scan avoids double counting. Derive row and column counters as you walk the array, or use nested loops.
