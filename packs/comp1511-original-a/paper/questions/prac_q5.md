# Q5 — Repair signed-number classification

## Background

The supplied program is intended to classify one integer, but its zero branch is incorrect.

## Requirements

Repair `prac_q5.c` so it reads exactly one integer and prints exactly one of `negative`, `zero`, or `positive`, followed by a newline. A value less than zero is negative; zero has its own classification; a value greater than zero is positive. Keep the existing input format and do not add prompts.

## Examples

```text
input:  -8     output: negative
input:   0     output: zero
input:  21     output: positive
```

## Implementation notes

Use mutually exclusive comparisons. Test values on both sides of zero as well as zero itself. Submit only `prac_q5.c`.

