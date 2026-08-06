# Fleet Components

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A board uses `#` for occupied cells and `.` for water. Orthogonally adjacent occupied cells belong to the same fleet component; diagonal contact alone does not connect them.

## Requirements

Write a complete C program in `c1511_core_038.c`.

**Input:** The first line contains rows and columns (1 <= rows, columns <= 20). The next rows lines each contain exactly columns characters.

**Output:** Print `components: k` and `largest: s`, where s is zero when there are no occupied cells.

**Assumptions:** The grid dimensions are small enough for recursive flood fill.

**Restrictions:** Store the board in a two-dimensional char array. Use four-directional traversal and do not count diagonal adjacency.

Submit exactly the file `c1511_core_038.c`.

## Examples

Input:

```text
3 5
##...
.#..#
....#
```

Output:

```text
components: 2
largest: 3
```

The three cells at left form one component and the two cells at right form another.

## Implementation notes

Mark a cell visited before recursively exploring neighbours so recursion cannot revisit it. Match every required label, space, punctuation mark, and newline exactly.

