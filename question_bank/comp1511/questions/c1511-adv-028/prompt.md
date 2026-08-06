# Recursive reverse copy

## Background

This original medium exercise combines several C concepts in one self-contained linked or dynamically allocated data task. `struct node *reverse_copy(const struct node *head)` recursively returns a deep copy whose order is the reverse of the input. The supplied harness constructs all input state and retains the ownership rules described below.

## Requirements

- Do not modify, relink, or free any input node.
- Allocate exactly one new node for each input node and copy every integer.
- Return `NULL` for empty input; the harness frees input and result independently.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

`./c1511_adv_028 1 2 3` prints `3 2 1` while the original list remains separately owned.

## Implementation notes

A recursive helper can carry the partially built reversed copy as an accumulator. Submit `c1511_adv_028.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source. The build uses the shell-free argument array `dcc -Werror <file> -o <program>`.
