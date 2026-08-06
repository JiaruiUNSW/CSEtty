# Record-high counter

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int count_record_highs(const struct node *head)` counts nodes whose value is strictly greater than every earlier value. The first node, when present, is a record.

## Requirements

- Visit nodes from left to right and do not mutate the list.
- Equal values do not establish a new record.
- Return `0` for an empty list and use no arrays or allocation inside the function.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_002 3 1 4 4 7` prints `3`, for the records 3, 4, and 7. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

Values may be negative. Modify only the marked function in the starter harness. Submit `c1511_adv_002.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
