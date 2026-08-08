# Streaming Total — solution guide

## Approach

Initialise index and sum to zero. While index is less than `n`, read the next integer, add it to the sum, and increment the index.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `mixed`, runs `mipsy c1521_low_007.s`.

Input:

```text
4
8
-3
5
2
```

Expected standard output:

```text
12
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The loop invariant states that the sum register contains exactly the first `index` values. When `index=n`, all and only the requested inputs have been accumulated.

## Complexity

O(n) time and O(1) extra storage.

## Common pitfalls

Do not include `n` itself in the sum. Check the loop condition before reading, otherwise the empty case consumes a nonexistent value.
