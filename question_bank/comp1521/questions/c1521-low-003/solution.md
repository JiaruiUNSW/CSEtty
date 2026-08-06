# Triangular Counter — solution guide

## Approach

Initialise the counter to one and the sum to zero. While the counter is at most `n`, add it to the sum and increment it.

## Correctness

Before each iteration, the accumulator is the sum of all positive integers smaller than the counter. The loop adds the counter and preserves this invariant. At termination the counter is `n+1`, so the accumulator is exactly `1+...+n`.

## Complexity

O(n) time and O(1) storage.

## Common pitfalls

A post-test loop often returns one for `n=0`. Also ensure the branch comparison is signed and the counter is incremented exactly once.
