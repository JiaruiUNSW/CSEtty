# Strictly Rising Columns — solution

## Approach

For each column, compare each row after the first with the row above; return false on a less-than-or-equal pair and true if the scan finishes.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `mixed`, runs `./c1511_core_009`.

Input:

```text
3 3
1 3 0
2 2 1
3 4 1
```

Expected standard output:

```text
rising columns: 1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

A column is strictly rising exactly when all adjacent comparisons are strict increases. The helper checks all and only those comparisons, so its answer is exact.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Equal neighbours invalidate strict increase. Handle one-row input without accessing row one. Also check every `scanf` target and preserve the required output format.
