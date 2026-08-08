# ASCII Class Code

## Background

Read one integer representing an ASCII code. Print 1 for a decimal digit, 2 for an uppercase letter, 3 for a lowercase letter, or 0 for anything else.

## Requirements

Use inclusive ASCII ranges `48..57`, `65..90`, and `97..122`. Print only the category number and newline.

Input constraints: 0 <= code <= 127.

Write your complete answer in `c1521_low_015.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
71
```

the exact output is:

```text
2
```

## Implementation notes

Implement an inclusive range test as two ordered comparisons. Once a class matches, branch to a shared print block.
