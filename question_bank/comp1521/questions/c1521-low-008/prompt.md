# Negative Reading Tally

## Background

Read `n`, followed by `n` signed readings. Print the number that are strictly negative.

This is an original local practice task. It exercises the `mips-control, integer-representation`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

Zero is not negative. Use signed comparison against zero and consume exactly the declared number of readings.

Input constraints: 0 <= n <= 50; each reading is a signed 32-bit integer.

Write your complete answer in `c1521_low_008.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
5
-2
0
7
-1
-9
```

the exact output is:

```text
3
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

The signed `slt` instruction can directly compute `value < 0` as a zero-or-one value that may be added to the count.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
