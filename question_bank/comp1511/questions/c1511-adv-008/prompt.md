# Stable odd-even relink

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *odd_before_even(struct node *head)` relinks nodes so all odd values precede all even values while preserving order within both groups.

## Requirements

- Classify negative odd values as odd and zero as even.
- Do not allocate, free, or change node data.
- Return the new head and terminate the final tail with `NULL`.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_008 4 1 3 2` prints `1 3 4 2`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

Detach each node before appending it to an odd or even chain. The harness frees the result. Submit `c1511_adv_008.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
