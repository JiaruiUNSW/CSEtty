# Longest Gentle Climb

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A hiking trace is divided into consecutive samples. A gentle climb is a contiguous run in which each new sample is greater than or equal to the previous sample.

## Requirements

Write a complete C program in `c1511_core_002.c`.

**Input:** The first line contains n (1 <= n <= 100). The next line contains n integer heights.

**Output:** Print `longest: k`, the length of the longest non-decreasing contiguous run.

**Assumptions:** All heights fit in a C `int`; a single sample is a run of length 1.

**Restrictions:** Use an array and a separate function for the longest-run calculation. Do not reorder the samples.

Submit exactly the file `c1511_core_002.c`.

## Examples

Input:

```text
6
1 2 2 0 3 4
```

Output:

```text
longest: 3
```

Both `1 2 2` and `0 3 4` have length 3.

## Implementation notes

Maintain the current run length and the best length seen. Reset the current length to 1 after a decrease. Your output must match the specified spelling, spacing, and newlines exactly.

