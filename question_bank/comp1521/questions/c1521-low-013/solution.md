# Threshold Exceedance Count — solution guide

## Approach

Read the count and threshold, then loop over the sequence and add one whenever the threshold is less than the current value.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `mixed`, runs `mipsy c1521_low_013.s`.

Input:

```text
5
10
11
10
-2
30
9
```

Expected standard output:

```text
2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

For each input, the signed predicate is one exactly when that input exceeds the threshold. Its accumulated sum is therefore the count requested.

## Complexity

O(n) time and O(1) extra storage.

## Common pitfalls

Reversing `slt` counts values below the threshold. Using `<=` incorrectly counts equal values.
