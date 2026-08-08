# Sign-Extend a Twelve-Bit Field

## Background

Read an unsigned hexadecimal value containing a 12-bit two's-complement field. Print the represented value as a signed decimal integer.

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

## Implementation notes

When bit `0x800` is set, OR with `0xfffff000`; otherwise the masked value is already positive.
