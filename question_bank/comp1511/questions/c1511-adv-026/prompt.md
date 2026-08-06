# Recursive threshold pruning

## Background

This original medium exercise combines several C concepts in one self-contained linked or dynamically allocated data task. `struct node *prune_below(struct node *head, int threshold)` recursively removes and frees nodes with values below the threshold. The supplied harness constructs all input state and retains the ownership rules described below.

## Requirements

- The first command-line value is the threshold; remaining values form the list.
- Retain qualifying nodes in original order and return the possibly new head.
- Free every rejected node exactly once and allocate no nodes.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

`./c1511_adv_026 3 1 3 5 2` prints `3 5`.

## Implementation notes

Recursively process the suffix, then either link it after the current survivor or free the current node. Submit `c1511_adv_026.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source. The build uses the shell-free argument array `dcc -Werror <file> -o <program>`.
