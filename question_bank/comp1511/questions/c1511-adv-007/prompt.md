# Keep first occurrences

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *keep_first_occurrences(struct node *head)` deletes every node whose value appeared earlier, preserving the first occurrence of each value.

## Requirements

- Preserve first-occurrence order and reuse surviving nodes.
- Free every removed node and allocate no arrays, lists, or lookup tables.
- The empty list remains empty.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_007 1 2 1 3 2
```

Output:

```text
1 2 3
```

## Implementation notes

An `O(n^2)` linked-list solution is expected and acceptable. The supplied `main` frees survivors. Submit `c1511_adv_007.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
