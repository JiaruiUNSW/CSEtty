# Count Even Samples

## Background

Read exactly five signed integers and print how many of them are even.

## Requirements

Use a loop to perform five reads. Test parity from the low bit; zero and negative even numbers count as even.

Input constraints: each sample is a signed 32-bit integer.

Write your complete answer in `c1521_low_006.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
1
2
3
4
6
```

the exact output is:

```text
3
```

## Implementation notes

`andi value, value, 1` isolates parity without needing division. Keep separate registers for the number read, the loop count, and the answer.
