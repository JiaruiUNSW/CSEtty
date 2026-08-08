# Stable odd-even relink

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *odd_before_even(struct node *head)` relinks nodes so all odd values precede all even values while preserving order within both groups.

## Requirements

- Classify negative odd values as odd and zero as even.
- Do not allocate, free, or change node data.
- Return the new head and terminate the final tail with `NULL`.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_008 4 1 3 2
```

Output:

```text
1 3 4 2
```

## Implementation notes

Detach each node before appending it to an odd or even chain. The supplied `main` frees the result. Submit `c1511_adv_008.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
