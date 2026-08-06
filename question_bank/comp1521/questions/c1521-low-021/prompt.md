# Interleave Two Coordinate Words

## Background

Read two 16-bit unsigned coordinates `x` and `y` in hexadecimal. Produce a 32-bit Morton code with `x` bit `i` at output bit `2i` and `y` bit `i` at output bit `2i+1`.

This is an original local practice task. It exercises the `bitwise, integer-representation`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Print exactly eight lowercase hexadecimal digits. Derive the code from the input bits; no lookup table covering complete answers is allowed.

Input constraints: 0x0000 <= x,y <= 0xffff.

Write your complete answer in `c1521_low_021.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
0003 0001
```

the exact output is:

```text
00000007
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

A straightforward 16-iteration loop is acceptable: isolate one bit from each input and shift it into its even or odd destination.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
