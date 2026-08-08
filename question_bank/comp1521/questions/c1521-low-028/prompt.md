# Classify a Binary32 Encoding

## Background

Read an eight-digit hexadecimal IEEE-754 binary32 bit pattern. Print one of `zero`, `subnormal`, `normal`, `infinity`, or `nan`.

## Requirements

Classify solely from the 8-bit exponent and 23-bit fraction. The sign bit does not change the class.

Input constraints: the input is any `uint32_t` bit pattern.

Write your complete answer in `c1521_low_028.c`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
7f800000
```

the exact output is:

```text
infinity
```

## Implementation notes

Extract exponent `(bits >> 23) & 0xff` and fraction `bits & 0x7fffff`. Exponent zero and all-ones are the special cases.
