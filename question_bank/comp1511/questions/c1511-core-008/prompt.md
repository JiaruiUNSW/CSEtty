# Frame Balance Checksum

## Background

A rectangular tile has an outer frame and an interior. Its frame balance checksum is the sum of border values minus the sum of all strictly interior values.

## Requirements

Write a complete C program in `c1511_core_008.c`.

**Input:** The first line contains rows and columns (2 <= rows, columns <= 20), followed by the integer tile values.

**Output:** Print `checksum: s`.

**Assumptions:** The checksum fits in a C `int`. For a two-row or two-column grid, there are no interior cells.

**Restrictions:** Store the tile as a two-dimensional array and classify each position exactly once.

Submit exactly the file `c1511_core_008.c`.

## Examples

Input:

```text
3 3
1 2 3
4 5 6
7 8 9
```

Output:

```text
checksum: 35
```

The border sums to 40 and the sole interior value is 5.

## Implementation notes

A cell is on the border when its row or column index is at either endpoint. Avoid summing corner cells twice. Your output must match the specified spelling, spacing, and newlines exactly.
