# Alternating chain weave

## Background

This original medium exercise combines several C concepts in one self-contained linked or dynamically allocated data task. `struct node *weave(struct node *left, struct node *right)` relinks two lists by alternating left then right nodes; any remainder follows unchanged. The supplied harness constructs all input state and retains the ownership rules described below.

## Requirements

- Command-line values before `--` build `left`; values after it build `right`; either side may be empty.
- Allocate and free no nodes inside the function, and preserve order within each source list.
- Return a single acyclic, null-terminated list beginning with left when available.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

`./c1511_adv_030 1 3 5 -- 2 4` prints `1 2 3 4 5`; `-- 7 8` prints `7 8`.

## Implementation notes

Save both next pointers before adding the current pair to the output. Exactly one delimiter is guaranteed. Submit `c1511_adv_030.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source. The build uses the shell-free argument array `dcc -Werror <file> -o <program>`.
