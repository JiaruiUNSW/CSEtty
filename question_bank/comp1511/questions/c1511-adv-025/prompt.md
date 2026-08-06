# Recursive neighbouring totals

## Background

This original medium exercise combines several C concepts in one self-contained linked or dynamically allocated data task. `struct node *pair_totals(const struct node *head)` recursively builds a new list containing the sum of each adjacent input pair; an unpaired final value is copied unchanged. The supplied harness constructs all input state and retains the ownership rules described below.

## Requirements

- Leave the input list and all its links unchanged.
- Allocate one result node per pair, plus one for an odd final node, and preserve pair order.
- Return `NULL` for empty input; the harness separately frees both lists.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

`./c1511_adv_025 1 2 3 4 5` prints `3 7 5`.

## Implementation notes

The recursive call can advance by two nodes when a pair exists. Assume each pair sum fits in `int`. Submit `c1511_adv_025.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source. The build uses the shell-free argument array `dcc -Werror <file> -o <program>`.
