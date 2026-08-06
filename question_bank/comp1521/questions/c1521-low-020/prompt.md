# Sign-Extend a Twelve-Bit Field

## Background

Read an unsigned hexadecimal value containing a 12-bit two's-complement field. Print the represented value as a signed decimal integer.

This is an original local practice task. It exercises the `integer-representation, bitwise, c-revision`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Mask to 12 bits and perform explicit sign extension from bit 11 into a `uint32_t`, then interpret the resulting bit pattern as `int32_t`.

Input constraints: 0x000 <= input <= 0xfff.

Write your complete answer in `c1521_low_020.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
f80
```

the exact output is:

```text
-128
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

When bit `0x800` is set, OR with `0xfffff000`; otherwise the masked value is already positive.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
