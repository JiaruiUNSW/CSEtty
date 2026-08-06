# Count Even Samples

## Background

Read exactly five signed integers and print how many of them are even.

This is an original local practice task. It exercises the `mips-control, bitwise`
part of COMP1521 without relying on any UNSW assessment text.

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

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

`andi value, value, 1` isolates parity without needing division. Keep separate registers for the number read, the loop count, and the answer.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
