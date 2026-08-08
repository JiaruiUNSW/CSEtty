# Add Two Readings

## Background

Translate a tiny arithmetic calculation into MIPS. Read two signed decimal integers, add them, and print their signed sum followed by a newline.

## Requirements

Use the integer input and output syscalls. Preserve the full 32-bit signed result; the supplied inputs are chosen so their mathematical sum is representable.

Input constraints: each input is between -100000 and 100000, and the sum fits in a signed 32-bit word.

Write your complete answer in `c1521_low_001.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
3
4
```

the exact output is:

```text
7
```

## Implementation notes

Keep both inputs in registers and use `addu` (or another non-trapping addition appropriate to the stated range). Print the newline with the character-output syscall.
