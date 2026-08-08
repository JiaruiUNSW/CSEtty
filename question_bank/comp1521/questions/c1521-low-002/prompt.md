# Absolute Sensor Gap

## Background

Read two signed sensor readings `a` and `b`, then print the non-negative distance `|a - b|` and a newline.

## Requirements

Compute the difference in registers, branch only when the sign requires negation, and print one decimal integer.

Input constraints: -10000 <= a,b <= 10000, so both the difference and its absolute value are representable in 32 bits.

Write your complete answer in `c1521_low_002.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
9
2
```

the exact output is:

```text
7
```

## Implementation notes

A zero or positive difference is already the answer. For a negative difference, subtract it from zero. The comparison must be signed.
