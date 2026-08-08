# Distance between first extremes

## Background

`size_t first_extreme_distance(const int *values, size_t length)` returns the index distance between the first minimum and first maximum.

## Requirements

- For zero or one value, return zero.
- When a minimum or maximum occurs repeatedly, use its first occurrence.
- Return the nonnegative absolute difference between their zero-based indices.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_021 4 1 7 1 7
```

Output:

```text
1
```

## Implementation notes

Use strict comparisons so ties retain their earlier indices. The input array is read-only. Submit `c1511_adv_021.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
