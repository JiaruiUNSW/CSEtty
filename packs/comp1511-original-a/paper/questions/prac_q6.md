# Q6 — Repair a natural-number sum

## Background

The program should accumulate every integer in an inclusive range, but the supplied accumulator is never updated.

## Requirements

Repair `prac_q6.c`. Read one integer `n` and print the sum `1 + 2 + ... + n` followed by a newline. You may assume `0 <= n <= 10000` and that the answer fits in an `int`. When `n` is zero, print `0`. Do not add input prompts or extra output.

## Examples

```text
input: 5       output: 15
input: 1       output: 1
input: 0       output: 0
input: 100     output: 5050
```

## Implementation notes

An inclusive loop beginning at one is sufficient. Check the loop condition carefully for the zero and one boundaries. Submit only `prac_q6.c`.

