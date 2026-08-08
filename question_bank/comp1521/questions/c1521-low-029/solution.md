# Recursive Binary Search — solution guide

## Approach

Save call state in a frame, check the empty range, and inspect the midpoint. Return it on equality; otherwise update either `high` or `low` and recursively search that smaller interval.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `present`, runs `mipsy c1521_low_029.s`.

Input:

```text
6
8
-3
0
4
8
12
20
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

If the midpoint differs from the target, strict ordering proves the target can occur only in the selected half. Each recursive range is smaller, and the empty range correctly represents absence, so the result is exactly the target index or -1.

## Complexity

O(log n) time and O(log n) stack space.

## Common pitfalls

Use signed comparisons because array values may be negative. An incorrect midpoint or unchanged bound causes infinite recursion; remember that even the not-found path must restore the frame.
