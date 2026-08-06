# First prefix threshold

## Background

This original exercise practises a small, precisely specified linked-list transformation or analysis. The supplied command-line harness converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int first_prefix_at_least(const struct node *head, int target)` returns the first zero-based index whose inclusive prefix sum is at least `target`, or `-1` if none exists.

## Requirements

- The first argument to the executable is the target; remaining arguments form the list.
- Test the prefix after adding each current node.
- Do not alter the nodes and do not assume values are positive.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

`./c1511_adv_003 6 2 1 3` prints `2`. `./c1511_adv_003 10 4 4` prints `-1`. List output uses one space between integers and a final newline; an empty list is printed as `EMPTY`.

## Implementation notes

The harness requires a target and reports usage with exit status 2 otherwise. Assume every prefix sum fits in `long`. Submit `c1511_adv_003.c`. The harness validates ownership by freeing all surviving nodes, so do not retain hidden aliases. Build commands are argument arrays and do not invoke a shell. Your submitted file must compile cleanly with `dcc -Werror`.
