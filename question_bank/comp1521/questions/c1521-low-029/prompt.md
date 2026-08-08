# Recursive Binary Search

## Background

Read `n`, target, then a strictly increasing array. Call `binary_search(base, low, high, target)` recursively and print its zero-based index, or -1 if absent.

## Requirements

Pass four arguments in `$a0`–`$a3`. Every recursive call must preserve `$ra`; the function itself performs no I/O.

Input constraints: 0 <= n <= 16; values are signed 32-bit integers; `high` begins at `n-1`.

Write your complete answer in `c1521_low_029.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
6
8
-3
0
4
8
12
20
```

the exact output is:

```text
3
```

## Implementation notes

The empty-range base case is `high < low`. Compute `mid = low + (high-low)/2`, load `base[mid]`, and recurse into exactly one half.
