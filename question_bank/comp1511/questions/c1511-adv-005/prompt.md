# Insert after the last even node

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *insert_after_last_even(struct node *head, int value)` allocates one node and inserts it after the final even-valued node.

## Requirements

- If there is no even-valued node, insert the new node at the front.
- The executable receives the inserted value first, followed by list values.
- Allocate exactly one new node and preserve every existing node's relative order.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_005 9 2 4 5` prints `2 4 9 5`; `./c1511_adv_005 8 1 3` prints `8 1 3`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

The supplied harness prints and frees the returned list. Treat zero and negative even values as even. Submit `c1511_adv_005.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
