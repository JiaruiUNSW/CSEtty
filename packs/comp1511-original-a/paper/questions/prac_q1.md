# Q1 — Count sign changes in a linked list

## Background

A sensor log has already been converted into a linked list of signed integers. A transition is interesting only when two adjacent, non-zero readings have opposite signs.

## Requirements

Complete `count_sign_changes` in `prac_q1.c`. Walk the supplied list and return the number of adjacent pairs for which one value is strictly negative and the other is strictly positive. A pair containing zero does not count. Do not allocate, free, reorder, or modify any node. An empty or one-node list returns `0`.

The supplied `main` converts command-line arguments into the list, prints the returned count followed by a newline, and frees the list. Do not change its observable behaviour.

## Examples

```text
./prac_q1 1 -2 -3 4
2

./prac_q1 -1 2 0 -4 5
2

./prac_q1 0 0 7
0
```

## Implementation notes

Stop when either the current node or its successor is `NULL`. Compare signs explicitly so integer multiplication cannot overflow. Submit only `prac_q1.c`.

