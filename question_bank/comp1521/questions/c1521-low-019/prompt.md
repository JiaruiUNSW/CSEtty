# Rotate a 32-Bit Word

## Background

Read a hexadecimal 32-bit word and a count `k`; rotate the word left by `k` bits and print eight lowercase hexadecimal digits.

This is an original local practice task. It exercises the `bitwise, integer-representation, c-revision`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Use unsigned shifts and explicitly handle `k=0`, for which the result is unchanged.

Input constraints: 0 <= k <= 31.

Write your complete answer in `c1521_low_019.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
80000001 1
```

the exact output is:

```text
00000003
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

For nonzero `k`, combine `value << k` with `value >> (32-k)`. Shifting a 32-bit object by 32 is undefined in C, which is why zero is separate.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
