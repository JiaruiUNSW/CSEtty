# Select a Byte

## Background

Read a 32-bit unsigned value in hexadecimal and an index `i`. Print byte `i`, where byte zero is the least-significant byte, as an unsigned decimal integer.

## Requirements

Use shifts and a byte mask. Input is accepted by `scanf` with the fixed-width hexadecimal format and output is decimal.

Input constraints: 0 <= i <= 3 and the hexadecimal value contains at most eight digits.

Write your complete answer in `c1521_low_017.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
1234abcd 1
```

the exact output is:

```text
171
```

## Implementation notes

Use `uint32_t`, shift right by `8*i`, then mask with `UINT32_C(0xff)`. Fixed-width `<inttypes.h>` macros avoid host-dependent formats.
