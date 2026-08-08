# Array Distance Function — solution guide

## Approach

Read the arrays, build a stack frame, and scan both pointers together. Each iteration computes one absolute difference and advances both addresses by four bytes.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `mixed`, runs `mipsy c1521_low_023.s`.

Input:

```text
3
1
8
-2
4
3
-2
```

Expected standard output:

```text
8
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At loop index `i`, the accumulator equals the distance contribution of indices below `i`. Adding `|A[i]-B[i]|` preserves the invariant; at `n`, it equals the complete array distance.

## Complexity

O(n) time and O(n) input storage; the function uses O(1) stack space.

## Common pitfalls

A function that changes `$s0`–`$s4` without saving them violates the ABI. Do not lose the original base addresses while reading the arrays.
