# Saturating Signed Addition

## Background

Read two signed 32-bit decimal integers. Print their mathematical sum, except clamp positive overflow to `INT32_MAX` and negative overflow to `INT32_MIN`.

This is an original local practice task. It exercises the `integer-representation, bitwise, c-revision`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Do not perform overflowing signed addition and do not use a wider integer type. Detect overflow from 32-bit unsigned bit patterns.

Input constraints: both inputs are valid `int32_t` values.

Write your complete answer in `c1521_low_022.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
2147483647 9
```

the exact output is:

```text
2147483647
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

Convert operands to `uint32_t`, add modulo 2^32, and compare operand/result sign bits. Overflow occurs only when equal-sign operands produce the opposite sign.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
