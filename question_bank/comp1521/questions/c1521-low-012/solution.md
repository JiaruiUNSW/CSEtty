# Sum of Squares by Function Call — solution guide

## Approach

Place the count, index, and accumulator in saved registers. Read each value into `$a0`, call the leaf multiplication function, and add its return value.

## Correctness

`square` returns `x*x` for its argument. The loop invariant makes the accumulator the sum of squares for all processed inputs; after `n` calls, it is the required total.

## Complexity

O(n) time and O(1) storage.

## Common pitfalls

Keeping the sum in `$t` registers while assuming a callee preserves them violates the convention. Use `mflo` after multiplication and handle `n=0`.
