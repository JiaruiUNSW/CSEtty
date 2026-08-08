# Deal nodes into two chains

## Background

`void deal_alternating(struct node *head, struct node **first, struct node **second)` moves nodes at even positions to `first` and odd positions to `second`.

## Requirements

- Preserve order within both output chains and allocate or free no nodes.
- Set both output pointers for every input, including the empty list.
- Terminate both chains with `NULL`; ownership transfers to the two outputs.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

Command:

```text
./c1511_adv_027 1 2 3 4 5
```

Output:

```text
A: 1 3 5
B: 2 4
```

## Implementation notes

A pointer-to-tail-link for each output avoids separate head cases. The supplied `main` prints and frees both results. Submit `c1511_adv_027.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source.
