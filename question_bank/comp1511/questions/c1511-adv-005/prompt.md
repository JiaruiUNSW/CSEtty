# Insert after the last even node

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *insert_after_last_even(struct node *head, int value)` allocates one node and inserts it after the final even-valued node.

## Requirements

- If there is no even-valued node, insert the new node at the front.
- The executable receives the inserted value first, followed by list values.
- Allocate exactly one new node and preserve every existing node's relative order.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_005 9 2 4 5
```

Output:

```text
2 4 9 5
```

## Implementation notes

The supplied `main` prints and frees the returned list. Treat zero and negative even values as even. Submit `c1511_adv_005.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
