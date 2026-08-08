# Triangular Counter

## Background

Read a non-negative integer `n` and print `1 + 2 + ... + n`. For `n = 0`, print zero.

## Requirements

Implement an explicit loop in MIPS. The output is one signed decimal integer followed by a newline.

Input constraints: 0 <= n <= 1000.

Write your complete answer in `c1521_low_003.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
5
```

the exact output is:

```text
15
```

## Implementation notes

Maintain a loop counter and an accumulator. Check the termination condition before adding so that the zero case performs no additions.
