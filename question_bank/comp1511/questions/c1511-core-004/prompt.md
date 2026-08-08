# Balanced Cut Counter

## Background

A row of cargo crates may be cut between adjacent crates. A cut is balanced when the total weight strictly to its left equals the total weight strictly to its right.

## Requirements

Write a complete C program in `c1511_core_004.c`.

**Input:** The first line contains n (2 <= n <= 100). The next line contains n integer weights.

**Output:** Print `balanced cuts: k`, counting valid cut positions.

**Assumptions:** Weights and all partial sums fit in a C `int`. Negative and zero weights are allowed.

**Restrictions:** Use an array and a helper function. A cut may only occur after positions 0 through n - 2.

Submit exactly the file `c1511_core_004.c`.

## Examples

Input:

```text
4
1 1 1 1
```

Output:

```text
balanced cuts: 1
```

Only the cut after the second crate leaves weight 2 on each side.

## Implementation notes

Compute the total once, then move values from the right sum into a running left sum. This avoids a nested loop. Your output must match the specified spelling, spacing, and newlines exactly.
