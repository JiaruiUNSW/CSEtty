# Consume an alternating checksum

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int consume_checksum(struct node *head)` returns `a0 - a1 + a2 - a3 + ...` while freeing the entire list.

## Requirements

- Read each value before freeing its node.
- Free every node exactly once, including when only one node remains.
- Return `0` for an empty list and leave no reachable allocation.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_012 5 2 1` prints `4`; no values print `0`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

The harness deliberately does not free the list after calling the function because ownership is transferred to it. Submit `c1511_adv_012.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
