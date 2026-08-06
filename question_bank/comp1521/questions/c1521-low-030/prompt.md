# Decode a MIPS R-Format Word

## Background

Read an eight-digit hexadecimal MIPS R-format instruction word. Print the decimal fields `rs rt rd shamt funct` separated by single spaces.

This is an original local practice task. It exercises the `mips-basics, bitwise, integer-representation`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Extract bits 25..21, 20..16, 15..11, 10..6, and 5..0. Inputs always have opcode zero.

Input constraints: the input is a valid 32-bit R-format word with bits 31..26 equal to zero.

Write your complete answer in `c1521_low_030.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
012a4020
```

the exact output is:

```text
9 10 8 0 32
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

Shift each field down to bit zero before masking it with `0x1f`, except `funct`, which uses six bits and mask `0x3f`.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
