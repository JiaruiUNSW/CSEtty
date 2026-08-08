# Apply Set and Clear Masks

## Background

Read three eight-digit hexadecimal words: `value`, `set_mask`, and `clear_mask`. First set every selected bit, then clear every selected bit, and print the final word in lowercase hexadecimal.

## Requirements

Compute `(value | set_mask) & ~clear_mask`. Clearing wins when the same bit appears in both masks. Print exactly eight hex digits.

Input constraints: all inputs fit in `uint32_t`.

Write your complete answer in `c1521_low_018.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
0000000a 00000005 00000008
```

the exact output is:

```text
00000007
```

## Implementation notes

Use fixed-width unsigned operations. The field width and leading-zero flag in `printf` make output deterministic.
