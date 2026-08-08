# Negative Reading Tally — solution guide

## Approach

Loop over all readings, evaluate a signed less-than-zero predicate for each, and add that predicate to the tally.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `mixed`, runs `mipsy c1521_low_008.s`.

Input:

```text
5
-2
0
7
-1
-9
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The predicate contributes one exactly for a negative input and zero otherwise. Summing it over the full sequence therefore gives precisely the number of negative readings.

## Complexity

O(n) time and O(1) extra storage.

## Common pitfalls

Using an unsigned comparison makes every value non-negative. Do not treat zero as negative or stop early when the tally reaches a particular number.
