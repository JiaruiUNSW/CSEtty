# Diagonal Colour Changes

## Background

A square mosaic's main diagonal is read from the top-left to the bottom-right. A colour change occurs whenever a diagonal value differs from the preceding diagonal value.

## Requirements

Write a complete C program in `c1511_core_010.c`.

**Input:** The first line contains n (1 <= n <= 20), followed by an n by n integer mosaic.

**Output:** Print `diagonal changes: k`.

**Assumptions:** Each integer denotes one colour code.

**Restrictions:** Store the complete mosaic in a two-dimensional array. Only main-diagonal neighbours are compared.

Submit exactly the file `c1511_core_010.c`.

## Examples

Input:

```text
4
1 9 9 9
8 1 8 8
7 7 2 7
6 6 6 3
```

Output:

```text
diagonal changes: 2
```

The diagonal is 1, 1, 2, 3, so it changes twice.

## Implementation notes

Begin comparisons at diagonal index one. A size-one mosaic has zero changes. Your output must match the specified spelling, spacing, and newlines exactly.
