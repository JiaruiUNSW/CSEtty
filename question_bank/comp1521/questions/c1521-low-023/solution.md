# Array Distance Function — solution guide

## Approach

Read the arrays, build a stack frame, and scan both pointers together. Each iteration computes one absolute difference and advances both addresses by four bytes.

## Correctness

At loop index `i`, the accumulator equals the distance contribution of indices below `i`. Adding `|A[i]-B[i]|` preserves the invariant; at `n`, it equals the complete array distance.

## Complexity

O(n) time and O(n) input storage; the function uses O(1) stack space.

## Common pitfalls

A function that changes `$s0`–`$s4` without saving them violates the ABI. Do not lose the original base addresses while reading the arrays.
