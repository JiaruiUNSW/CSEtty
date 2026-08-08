# Buffered Dot Product

## Background

Read a length `n`, then all `n` elements of vector A, then all `n` elements of vector B. Print their dot product.

## Requirements

Store vector A in memory because B arrives later. Compute `sum(A[i] * B[i])` in index order and print the signed result.

Input constraints: 0 <= n <= 16; values and the final dot product are within signed 32-bit range.

Write your complete answer in `c1521_low_010.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
3
1
2
3
4
5
6
```

the exact output is:

```text
32
```

## Implementation notes

Reserve 64 bytes of aligned storage. Scale each index by four before adding it to the base address. Use `mult` and `mflo` for each product.
