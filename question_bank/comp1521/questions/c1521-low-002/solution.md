# Absolute Sensor Gap — solution guide

## Approach

Subtract `b` from `a`. Test the sign of the result; negate it only when it is negative, then print it.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `descending`, runs `mipsy c1521_low_002.s`.

Input:

```text
9
2
```

Expected standard output:

```text
7
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

If `a-b` is non-negative, it equals `|a-b|`. If it is negative, its negation equals `b-a`, which is `|a-b|`. The branch selects exactly these two cases.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Reversing the subtraction happens to pass some cases but not all. Use a signed sign test and respect the stated range rather than attempting to handle `INT_MIN`.
