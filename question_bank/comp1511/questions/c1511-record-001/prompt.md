# First Highest Lab Batch

## Task

Return the zero-based index of the first maximum-valued record, or -1 when there are none.

## Background

Named records combine a short identifier with one signed measurement. The identifier establishes the input shape while the required result uses record order and values.

## Requirements

Read `n` (0 to 50), followed by `n` lines containing a whitespace-free name and signed value. Print `result: X`.

## Starter code

Complete `static long long solve(const struct record *a, int n)`. The supplied `main` reads the records and prints the returned value.

## Examples

Input:

```text
4
a 3
b -1
c 3
d 8
```

Output:

```text
result: 3
```

## Implementation notes

Represent each item with a `struct`; use a width limit when scanning the 31-character name.

## Submission

Submit `c1511_record_001.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
