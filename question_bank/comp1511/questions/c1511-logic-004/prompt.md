# Largest Absolute Offset

## Task

Return the largest absolute magnitude among the three signed inputs.

## Background

A small control program receives three signed readings and must make one deterministic decision. Equality and signed boundary cases are intentional.

## Requirements

Read exactly three signed integers from standard input. Print the computed value as `result: X` followed by one newline.

## Starter code

Complete `static long long solve(int a, int b, int c)`. The supplied `main` reads the three inputs and prints the returned value.

## Examples

Input:

```text
-4 9 2
```

Output:

```text
result: 9
```

## Implementation notes

Use named intermediate values when that makes the tie rule visible. Do not rely on undefined signed overflow.

## Submission

Submit `c1511_logic_004.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
