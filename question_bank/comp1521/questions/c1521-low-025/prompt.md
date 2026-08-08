# Decode Packed Sensor Records

## Background

Read `n` packed 32-bit records. Bits 0..7 are an unsigned score and bits 8..15 are a signed eight-bit adjustment. Print the sum of scores, then the sum of adjustments, each on its own line.

## Requirements

Extract fields with shifts and masks. Sign-extend the adjustment from eight bits; ignore bits 16..31.

Input constraints: 0 <= n <= 20 and both output sums fit signed 32 bits.

Write your complete answer in `c1521_low_025.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
2
2688
61441
```

the exact output is:

```text
129
-6
```

## Implementation notes

After shifting the adjustment into bits 0..7, sign-extend by shifting it left 24 and arithmetically right 24.
