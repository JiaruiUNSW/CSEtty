# Matrix Border Sum — solution guide

## Approach

Store the matrix, then use nested row and column loops. Add a cell when its row is zero or `rows-1`, or its column is zero or `cols-1`.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `square`, runs `mipsy c1521_low_027.s`.

Input:

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

Expected standard output:

```text
40
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The condition is true exactly for cells on at least one of the four boundaries. Each cell is visited once, so corners and degenerate dimensions are included once rather than once per matching edge.

## Complexity

O(rows*cols) time and O(rows*cols) input storage, with O(1) stack space.

## Common pitfalls

Summing four edges independently double-counts corners and badly mishandles one-row matrices. Compute byte offsets as `(row*cols+col)*4`.
