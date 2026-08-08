# Streaming Total

## Background

Read a count `n`, then read `n` signed integers and print their sum. An empty sequence has sum zero.

## Requirements

Consume exactly `n` values after the count. Use a counted loop and print one signed result with newline.

Input constraints: 0 <= n <= 30 and the mathematical sum fits in a signed 32-bit word.

Write your complete answer in `c1521_low_007.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
4
8
-3
5
2
```

the exact output is:

```text
12
```

## Implementation notes

The values do not need to be stored: accumulate each as soon as it is read. A loop-index comparison naturally handles `n=0`.
