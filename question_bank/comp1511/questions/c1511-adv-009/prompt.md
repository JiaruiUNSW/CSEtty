# Bridge adjacent values

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *insert_pair_sums(struct node *head)` inserts a new node between every originally adjacent pair; its value is the pair's sum.

## Requirements

- Inserted nodes must not themselves create further insertions.
- Lists of length zero or one are unchanged.
- Allocate one bridge per original adjacency and preserve all original nodes.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_009 1 2 3
```

Output:

```text
1 3 2 5 3
```

## Implementation notes

Assume each adjacent sum fits in `int`. Save the original right neighbour before linking the bridge. Submit `c1511_adv_009.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
