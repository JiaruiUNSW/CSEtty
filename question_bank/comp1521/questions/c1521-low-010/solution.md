# Buffered Dot Product — solution guide

## Approach

First loop reads and stores A. A second loop reads each B value, loads the matching A element, multiplies the pair, and accumulates the product.

## Correctness

The first loop establishes that memory slot `i` contains `A[i]`. After `k` iterations of the second loop, the accumulator is the sum of the first `k` pairwise products. At `k=n` this is the required dot product.

## Complexity

O(n) time and O(n) reserved data memory, bounded at 64 bytes.

## Common pitfalls

Reading A and B as alternating pairs violates the specified input order. Multiply the index by four and reset the index before the second loop.
