# Q3 — Delete the first negative node

## Background

A linked sequence may contain one invalid negative reading. Only the first such node should be removed; later values must remain untouched.

## Requirements

Complete `delete_first_negative` in `prac_q3.c`. Return the possibly changed head of the list. If a negative node exists, unlink the first one, free exactly that node, and preserve the order and values of all other nodes. If no negative node exists, return the original head. The function must handle an empty list and a negative head.

The harness builds the list from command-line arguments. It prints the remaining values separated by spaces, or `empty` when no nodes remain.

## Examples

```text
./prac_q3 1 -2 3
1 3

./prac_q3 -1 2 3
2 3

./prac_q3 -7
empty
```

## Implementation notes

Keep a pointer to the predecessor or use a pointer-to-pointer so the head case follows the same update rule as an interior deletion. Save the removed node before relinking, then free it once. Submit `prac_q3.c`.

