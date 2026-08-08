# Buffered Dot Product — solution guide

## Approach

First loop reads and stores A. A second loop reads each B value, loads the matching A element, multiplies the pair, and accumulates the product.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `three`, runs `mipsy c1521_low_010.s`.

Input:

```text
3
1
2
3
4
5
6
```

Expected standard output:

```text
32
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The first loop establishes that memory slot `i` contains `A[i]`. After `k` iterations of the second loop, the accumulator is the sum of the first `k` pairwise products. At `k=n` this is the required dot product.

## Complexity

O(n) time and O(n) reserved data memory, bounded at 64 bytes.

## Common pitfalls

Reading A and B as alternating pairs violates the specified input order. Multiply the index by four and reset the index before the second loop.
