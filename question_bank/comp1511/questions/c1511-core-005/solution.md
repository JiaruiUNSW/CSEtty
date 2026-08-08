# Calm Grid Rows — solution

## Approach

For each row, scan its columns to obtain a minimum and maximum, compare their difference with the tolerance, and count successful rows.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `one-calm`, runs `./c1511_core_005`.

Input:

```text
2 3 2
1 2 3
5 8 6
```

Expected standard output:

```text
calm rows: 1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The helper examines every value in a row, so its extrema and range are exact. The outer loop counts exactly those rows whose exact range meets the calm condition.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Negative values make zero a bad extrema sentinel. Use `<= tolerance`, not a strict comparison. Also check every `scanf` target and preserve the required output format.
