# Consume an alternating checksum

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int consume_checksum(struct node *head)` returns `a0 - a1 + a2 - a3 + ...` while freeing the entire list.

## Requirements

- Read each value before freeing its node.
- Free every node exactly once, including when only one node remains.
- Return `0` for an empty list and leave no reachable allocation.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_012 5 2 1
```

Output:

```text
4
```

## Implementation notes

The supplied `main` deliberately does not free the list after calling the function because ownership is transferred to it. Submit `c1511_adv_012.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
