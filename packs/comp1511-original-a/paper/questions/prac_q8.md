# Q8 — Count digit nodes

## Background

The harness converts a command-line string into a linked list with one character per node.

## Requirements

Complete `count_digits` in `prac_q8.c`. Return the number of nodes whose value is an ASCII digit from `'0'` through `'9'` inclusive. Do not count punctuation, signs, spaces, or letters. Do not modify, allocate, or free nodes inside the function. An empty list returns `0`.

The supplied `main` builds and later frees the list, then prints the returned count.

## Examples

```text
./prac_q8 a1b20
3

./prac_q8 letters
0

./prac_q8 007
3
```

## Implementation notes

Traverse until `NULL` and use an inclusive character-range test. The integer value represented by the string is irrelevant; count nodes, not distinct digits. Submit `prac_q8.c`.

