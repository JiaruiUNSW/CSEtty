# Remove the first debt

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *remove_first_negative(struct node *head)` removes and frees only the first node whose value is negative.

## Requirements

- Return the possibly changed head.
- If no value is negative, return the original list unchanged.
- Free the removed node exactly once; never allocate a replacement.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_006 2 -3 4` prints `2 4`; `./c1511_adv_006 -1` prints `EMPTY`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

The harness owns and frees all nodes still reachable from the returned head. Modify only `solve`. Submit `c1511_adv_006.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
