# Alternating-position total

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int alternating_position_total(const struct node *head)` returns the sum of values at zero-based positions 0, 2, 4, and so on.

## Requirements

- Traverse the list once without changing any node or link.
- An empty list returns `0`; position zero is included.
- Use the supplied `main`, list builder, printer-freeing helpers, and change only the marked function.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Running `./c1511_adv_001 4 7 1 9` prints `5`. Running it with no values prints `0`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

Assume the mathematical result fits in an `int`. Do not allocate memory, use arrays, or count the list in a separate pass. Submit `c1511_adv_001.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
