# Even Platform Codes

## Task

Count elements whose remainder modulo 2 is zero, including zero and negative evens.

## Background

The data comes from a railway platform audit and is stored as a bounded integer array. The array order is significant whenever the task refers to positions or neighbours.

## Requirements

Read `n` (0 to 100), followed by `n` signed integers. Print the computed value as `result: X` followed by a newline. The task rule states the result for an empty array whenever `n = 0` is valid.

## Starter code

Complete `static long long solve(const int *a, int n)`. The supplied `main` already reads the array and prints the returned value; do not replace the input/output code.

## Examples

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
result: 3
```

## Implementation notes

Use the supplied array and helper function. Do not sort or alter the input unless the task explicitly depends on ordering. All supplied arithmetic fits in `long long`.

## Submission

Submit `c1511_array_003.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
