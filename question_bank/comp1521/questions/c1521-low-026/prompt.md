# Encode a MIPS I-Format Word

## Background

Read decimal fields `opcode rs rt immediate` and encode the standard MIPS I-format word. Print the result as eight lowercase hexadecimal digits.

## Requirements

Place the 6-bit opcode at 31..26, 5-bit `rs` at 25..21, 5-bit `rt` at 20..16, and the low 16 bits of signed `immediate` at 15..0.

Input constraints: 0 <= opcode <= 63, 0 <= rs,rt <= 31, and -32768 <= immediate <= 32767.

Write your complete answer in `c1521_low_026.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
8 9 10 -4
```

the exact output is:

```text
212afffc
```

## Implementation notes

Convert the immediate to `uint16_t` before widening it. Use unsigned fields so left shifts are defined.
