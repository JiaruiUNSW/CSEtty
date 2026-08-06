# Sensor Window Anomalies

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A sliding window over sensor readings is anomalous when its range, maximum minus minimum, is at least a supplied threshold. The report also records the greatest range among all windows.

## Requirements

Write a complete C program in `c1511_core_037.c`.

**Input:** The first line contains n, width, and threshold (1 <= width <= n <= 100; threshold >= 0). The next line contains n integer readings.

**Output:** Print `anomalies: k` and `maximum range: r`.

**Assumptions:** Every range fits in a C `int`.

**Restrictions:** Store readings in an array and use a helper to calculate the range beginning at a supplied index.

Submit exactly the file `c1511_core_037.c`.

## Examples

Input:

```text
5 3 4
1 4 2 8 7
```

Output:

```text
anomalies: 2
maximum range: 6
```

The last two width-three windows have range six; the first has range three.

## Implementation notes

There are n - width + 1 windows. Initialise the maximum from the first window. Match every required label, space, punctuation mark, and newline exactly.

