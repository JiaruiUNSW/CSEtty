# Collapse sign regions

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *collapse_sign_regions(struct node *head)` replaces each maximal consecutive region of negative or nonnegative values with its sum.

## Requirements

- Reuse the first node of each region and free every additional node in that region.
- Zero belongs to the nonnegative class.
- Do not allocate nodes; preserve the order of regions.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_010 2 -1 -3 4 5
```

Output:

```text
2 -4 9
```

## Implementation notes

Assume every regional sum fits in `int`. The result is printed and freed by the supplied `main`. Submit `c1511_adv_010.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
