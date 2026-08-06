# Bridge adjacent values

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *insert_pair_sums(struct node *head)` inserts a new node between every originally adjacent pair; its value is the pair's sum.

## Requirements

- Inserted nodes must not themselves create further insertions.
- Lists of length zero or one are unchanged.
- Allocate one bridge per original adjacency and preserve all original nodes.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_009 1 2 3` prints `1 3 2 5 3`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

Assume each adjacent sum fits in `int`. Save the original right neighbour before linking the bridge. Submit `c1511_adv_009.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
