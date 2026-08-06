# Clamp a Control Value

## Background

Read signed integers `value`, `low`, and `high`. Print `low` when `value < low`, `high` when `value > high`, and otherwise print `value`.

This is an original local practice task. It exercises the `mips-control, integer-representation`
part of COMP1521 without relying on any UNSW assessment text.

## Requirements

All comparisons must be signed, and the output must contain exactly the clamped decimal value plus newline.

Input constraints: `low <= high`; every input is a signed 32-bit integer.

Write your complete answer in `c1521_low_005.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
18
0
10
```

the exact output is:

```text
10
```

The public examples illustrate the interface only; marking also uses distinct
boundary and mixed-value cases.

## Implementation notes

The lower-bound and upper-bound cases are mutually exclusive once `low <= high` is known. Structure the branches so the in-range path remains clear.

Do not special-case the shown values or embed a table of test answers. Your
algorithm must work for every value permitted by the constraints.
