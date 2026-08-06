# Rotate an Eight-Bit Dial

## Background

Read an unsigned byte value `x` in decimal and a rotation count `k`. Rotate the low eight bits of `x` left by `k`, then print the resulting unsigned byte in decimal.

This is an original local practice task. It exercises the `bitwise, mips-control, integer-representation`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Implement `(x << k) | (x >> (8-k))`, mask the result to eight bits, and handle `k=0` without shifting by eight.

Input constraints: 0 <= x <= 255 and 0 <= k <= 7.

Write your complete answer in `c1521_low_014.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
129
1
```

the exact output is:

```text
3
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

Use variable shifts `sllv` and `srlv`. Branch around the second expression for `k=0`, then apply an `0xff` mask.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
