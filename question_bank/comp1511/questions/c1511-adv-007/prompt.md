# Keep first occurrences

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *keep_first_occurrences(struct node *head)` deletes every node whose value appeared earlier, preserving the first occurrence of each value.

## Requirements

- Preserve first-occurrence order and reuse surviving nodes.
- Free every removed node and allocate no arrays, lists, or lookup tables.
- The empty list remains empty.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_007 1 2 1 3 2` prints `1 2 3`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

An `O(n^2)` linked-list solution is expected and acceptable. The harness frees survivors. Submit `c1511_adv_007.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
