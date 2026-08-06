# Count Echo Valleys

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A sensor log is stored as a sequence of integer readings. An interior reading is an echo valley when it is strictly lower than the reading immediately before it and the reading immediately after it.

## Requirements

Write a complete C program in `c1511_core_001.c`.

**Input:** The first line contains n (3 <= n <= 100). The next line contains n integer readings.

**Output:** Print `valleys: k`, where k is the number of echo valleys.

**Assumptions:** Every reading fits in a C `int`. The first and last readings are never counted because they do not have two neighbours.

**Restrictions:** Store the readings in an array and implement the counting step in a separate function. Do not sort or modify the readings.

Submit exactly the file `c1511_core_001.c`.

## Examples

Input:

```text
5
4 1 3 2 5
```

Output:

```text
valleys: 2
```

The readings 1 and 2 are each lower than both immediate neighbours.

## Implementation notes

Scan only indices 1 through n - 2. Strict comparisons matter: an equal neighbour prevents a valley. Your output must match the specified spelling, spacing, and newlines exactly.

