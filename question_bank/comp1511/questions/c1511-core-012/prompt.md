# Shifted Signal Mismatches

This is an original C programming task for the local CSEExamTTY simulator.

## Background

Two cyclic signals contain the same number of samples. The first signal is viewed after a left rotation, and it must be compared position-by-position with the second signal.

## Requirements

Write a complete C program in `c1511_core_012.c`.

**Input:** The first line contains n and shift (1 <= n <= 100, 0 <= shift < n). The next two lines contain n integers for signals A and B.

**Output:** Print `mismatches: k`, where A[(i + shift) modulo n] is compared with B[i].

**Assumptions:** Every sample fits in a C `int`.

**Restrictions:** Store both arrays, use modulo indexing, and do not physically rotate or reorder either array.

Submit exactly the file `c1511_core_012.c`.

## Examples

Input:

```text
4 1
1 2 3 4
2 3 4 1
```

Output:

```text
mismatches: 0
```

A viewed one position to the left is exactly B.

## Implementation notes

The index calculation must wrap for positions near the end. Shift zero is a direct comparison. Your output must match the specified spelling, spacing, and newlines exactly.

