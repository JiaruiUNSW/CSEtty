# Maximum Bracket Nesting

## Task

Return the maximum parenthesis nesting depth, or -1 if any prefix closes below zero or the final depth is nonzero.

## Background

A line-oriented tool must summarise human-readable text. The complete line, including spaces, is meaningful.

## Requirements

Read one line of at most 255 characters, excluding the final newline from the calculation. Print `result: X` and a newline. Character classification is ASCII for these tests.

## Starter code

Complete `static long long solve(const char *s)`. The supplied `main` reads one line, removes its trailing newline, and prints the returned value.

## Examples

Input:

```text
A1 beta
```

Output:

```text
result: 0
```

## Implementation notes

Use `fgets`, remove at most one trailing newline, and cast to `unsigned char` before calling `<ctype.h>` functions.

## Submission

Submit `c1511_text_008.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
