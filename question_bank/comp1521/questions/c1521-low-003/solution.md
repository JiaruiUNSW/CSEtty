# Triangular Counter — solution guide

## Approach

Initialise the counter to one and the sum to zero. While the counter is at most `n`, add it to the sum and increment it.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `five`, runs `mipsy c1521_low_003.s`.

Input:

```text
5
```

Expected standard output:

```text
15
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Before each iteration, the accumulator is the sum of all positive integers smaller than the counter. The loop adds the counter and preserves this invariant. At termination the counter is `n+1`, so the accumulator is exactly `1+...+n`.

## Complexity

O(n) time and O(1) storage.

## Common pitfalls

A post-test loop often returns one for `n=0`. Also ensure the branch comparison is signed and the counter is incremented exactly once.
