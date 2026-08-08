# Unique Column Beacons — solution

## Approach

Scan each column from top to bottom, tracking the largest value and how many times it occurs, then count the column if the occurrence count is one.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `ties`, runs `./c1511_core_006`.

Input:

```text
3 3
1 5 2
4 5 3
0 2 3
```

Expected standard output:

```text
unique beacons: 1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After each row, the tracked value is the maximum of the visited prefix and the count is its exact multiplicity. At column end, count one therefore means precisely a unique maximum.

## Complexity

O(rows * columns) time and O(rows * columns) grid storage.

## Common pitfalls

When finding a new larger value, reset the occurrence count. Equal maxima must increase it. Also check every `scanf` target and preserve the required output format.
