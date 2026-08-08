# Sum of Squares by Function Call — solution guide

## Approach

Place the count, index, and accumulator in saved registers. Read each value into `$a0`, call the leaf multiplication function, and add its return value.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `mixed`, runs `mipsy c1521_low_012.s`.

Input:

```text
3
2
-3
4
```

Expected standard output:

```text
29
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

`square` returns `x*x` for its argument. The loop invariant makes the accumulator the sum of squares for all processed inputs; after `n` calls, it is the required total.

## Complexity

O(n) time and O(1) storage.

## Common pitfalls

Keeping the sum in `$t` registers while assuming a callee preserves them violates the convention. Use `mflo` after multiplication and handle `n=0`.
