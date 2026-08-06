# Array Distance Function

## Background

Read `n`, vector A, then vector B. Call `array_distance(A, B, n)` to return the sum of `|A[i]-B[i]|`, then print it.

This is an original local practice task. It exercises the `mips-functions, mips-data, integer-representation`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

The function receives pointers in `$a0/$a1`, length in `$a2`, saves every `$s` register it changes, restores `$sp`, and performs no I/O.

Input constraints: 0 <= n <= 12; differences and their sum fit signed 32 bits.

Write your complete answer in `c1521_low_023.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
3
1
8
-2
4
3
-2
```

the exact output is:

```text
8
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

Store both arrays in separate aligned regions. Inside the function, take an absolute difference before adding it to the accumulator.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
