# Largest of Three

## Background

Read three signed decimal integers and print the largest value, followed by a newline.

## Requirements

Use signed comparisons. Equal values are allowed, and any occurrence of the maximum may determine the result.

Input constraints: all three values are valid signed 32-bit integers.

Write your complete answer in `c1521_low_004.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
4
12
7
```

the exact output is:

```text
12
```

## Implementation notes

Start with the first input as the candidate. Compare each later value against the candidate and replace it only if it is larger.
