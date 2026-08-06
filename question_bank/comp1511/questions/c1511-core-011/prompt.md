# Stable Sentinel Removal

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A data stream has been copied into an array, but a chosen sentinel value represents missing samples. The valid samples must be compacted toward the front without changing their order.

## Requirements

Write a complete C program in `c1511_core_011.c`.

**Input:** The first line contains n and sentinel (1 <= n <= 100), followed by n integer samples.

**Output:** Print retained samples on one space-separated line with no trailing space, then print `kept: k` on the next line. Print an empty first line if none remain.

**Assumptions:** All inputs fit in a C `int`.

**Restrictions:** Compact the array in place using a helper function. Do not create a second sample array and do not sort.

Submit exactly the file `c1511_core_011.c`.

## Examples

Input:

```text
6 -1
3 -1 4 -1 5 6
```

Output:

```text
3 4 5 6
kept: 4
```

The two sentinel entries are removed while the other four retain their order.

## Implementation notes

A write index identifies the next retained position. It advances only when a non-sentinel item is copied. Your output must match the specified spelling, spacing, and newlines exactly.

