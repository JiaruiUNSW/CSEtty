# Distance-Weighted Supply Chain

## Task

Compute `sum((position + 1) * value)` in list order.

## Background

A linked chain stores readings in arrival order. The supplied `main` owns the nodes and frees the complete chain after `solve` returns.

## Requirements

Each command-line integer becomes one list node in the same order. With no arguments, `head` is `NULL`. Return the required value from `solve`; the supplied `main` prints it as `result: X`.

## Starter code

Complete `static long long solve(const struct node *head)`. The supplied `main` builds and later frees the list; `solve` must inspect it without changing ownership.

## Examples

Command-line arguments: `3 -1 -1 4 0 -2`

Output:

```text
result: 2
```

## Implementation notes

Do not change `main` or print inside `solve`. Preserve every `next` link. Recursive variants should give the empty-list base case before accessing a node.

## Submission

Submit `c1511_list_010.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
