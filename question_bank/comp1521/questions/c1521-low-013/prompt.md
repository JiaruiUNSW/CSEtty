# Threshold Exceedance Count

## Background

Read `n`, then a threshold `t`, then `n` signed values. Print how many values are strictly greater than `t`.

## Requirements

Use a signed comparison and a counted loop. Equality does not count.

Input constraints: 0 <= n <= 40; all values and the threshold are signed 32-bit integers.

Write your complete answer in `c1521_low_013.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
5
10
11
10
-2
30
9
```

the exact output is:

```text
2
```

## Implementation notes

`slt result, threshold, value` computes the required predicate directly. Add the zero-or-one result to the tally.
