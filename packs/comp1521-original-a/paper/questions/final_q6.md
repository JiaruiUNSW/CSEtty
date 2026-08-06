# Q6 — Count set bits in MIPS

## Background

The population count of a word is the number of bit positions containing 1.
For example, the low four bits of decimal 15 are `1111`, so its population
count is 4. A signed input still represents a complete 32-bit two's-complement
word.

## Program requirements

Complete `final_q6.s` so that it:

- reads one signed 32-bit integer;
- examines all 32 bit positions;
- prints the number of set bits followed by a newline; and
- exits normally.

Use a loop and bitwise operations. The solution must terminate after exactly 32
iterations even when the input is negative. Do not use a lookup table or print
extra text.

## Examples

```text
$ printf '15\n' | mipsy final_q6.s
4
$ printf '%s\n' -1 | mipsy final_q6.s
32
```

## Implementation notes

Masking the low bit and then using a logical right shift avoids sign extension.
A separate loop counter is needed because shifting `-1` arithmetically would
never reach zero.

