# Recursive Triangular Function — solution guide

## Approach

Return zero directly for the base case. Otherwise save call state, recurse on `n-1`, add the saved `n` to the returned partial sum, and unwind the frame.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `six`, runs `mipsy c1521_low_024.s`.

Input:

```text
6
```

Expected standard output:

```text
21
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

By induction, the base returns the empty sum. Assuming the recursive call returns `1+...+(n-1)`, adding `n` returns `1+...+n`; therefore all permitted inputs are correct.

## Complexity

O(n) time and O(n) stack space.

## Common pitfalls

A recursive `jal` overwrites `$ra`. Restoring the argument from an incorrect offset or failing to deallocate the frame corrupts later returns.
