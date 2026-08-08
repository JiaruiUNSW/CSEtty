# First Maximum Index

## Background

Read `n` and then `n` signed integers into an array. Call `first_max_index(array, n)` and print the zero-based index of the first maximum.

## Requirements

Pass the base address in `$a0` and length in `$a1`. The function returns the index in `$v0`; it must not perform I/O.

Input constraints: 1 <= n <= 16; every element is a signed 32-bit integer.

Write your complete answer in `c1521_low_016.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
5
3
9
2
9
4
```

the exact output is:

```text
1
```

## Implementation notes

Reserve 64 aligned bytes. Update the saved index only for a strictly larger element so that ties retain the first occurrence.
