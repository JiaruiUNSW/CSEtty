# Encode a Compact MIPS I-Format Word

## Task

Encode opcode=`x & 63`, rs=`y & 31`, rt=`k & 31`, and immediate=`(x ^ y) & 65535` into the standard MIPS I-format bit positions.

## Background

A systems utility represents compact state in one 32-bit word. The transformation must be explicit about unsigned shifts, masks, and field widths.

## Requirements

Read two hexadecimal 32-bit words `x y` and a decimal shift or field value `k`. Print the computed value as `result: XXXXXXXX` using exactly eight lowercase hexadecimal digits.

## Starter code

Complete `static uint32_t solve(uint32_t x, uint32_t y, unsigned k)`. The supplied `main` reads the values and prints the returned word in the required format.

## Examples

Input:

```text
12345678 00ff00ff 8
```

Output:

```text
result: e3e85687
```

## Implementation notes

Use `uint32_t`. Reduce variable shifts to 0 through 31 before shifting, and never shift a 32-bit value by 32.

## Submission

Submit `c1521_bits_019.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
