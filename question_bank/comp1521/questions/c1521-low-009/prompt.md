# Euclidean Pair

## Background

Read two positive integers `a` and `b` and print their greatest common divisor.

This is an original local practice task. It exercises the `mips-control, integer-representation`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Implement Euclid's remainder algorithm in a loop. Print one positive decimal integer and newline.

Input constraints: 1 <= a,b <= 1000000000.

Write your complete answer in `c1521_low_009.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
84
30
```

the exact output is:

```text
6
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

MIPS division places the remainder in `HI`; use `mfhi` before issuing another division. Replace `(a,b)` by `(b,a mod b)`.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
