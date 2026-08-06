# Recursive Triangular Function — solution guide

## Approach

Return zero directly for the base case. Otherwise save call state, recurse on `n-1`, add the saved `n` to the returned partial sum, and unwind the frame.

## Correctness

By induction, the base returns the empty sum. Assuming the recursive call returns `1+...+(n-1)`, adding `n` returns `1+...+n`; therefore all permitted inputs are correct.

## Complexity

O(n) time and O(n) stack space.

## Common pitfalls

A recursive `jal` overwrites `$ra`. Restoring the argument from an incorrect offset or failing to deallocate the frame corrupts later returns.
