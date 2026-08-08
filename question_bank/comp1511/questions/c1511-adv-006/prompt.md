# Remove the first debt

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *remove_first_negative(struct node *head)` removes and frees only the first node whose value is negative.

## Requirements

- Return the possibly changed head.
- If no value is negative, return the original list unchanged.
- Free the removed node exactly once; never allocate a replacement.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_006 2 -3 4
```

Output:

```text
2 4
```

## Implementation notes

The supplied `main` owns and frees all nodes still reachable from the returned head. Modify only `remove_first_negative`. Submit `c1511_adv_006.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
