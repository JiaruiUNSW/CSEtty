# Sensor Window Anomalies — solution

## Approach

Enumerate every valid start index, compute that window's extrema and range, update the global maximum, and count ranges meeting the inclusive threshold.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `two`, runs `./c1511_core_037`.

Input:

```text
5 3 4
1 4 2 8 7
```

Expected standard output:

```text
anomalies: 2
maximum range: 6
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each possible fixed-width window is examined once and its helper range is exact. Counting qualifying exact ranges and taking their maximum gives both requested statistics.

## Complexity

O((n - width + 1) * width) time and O(n) space.

## Common pitfalls

Use at least rather than greater than for the threshold, include the final start index, and initialise extrema from a value inside each window. Verify boundary inputs as well as the worked example.
