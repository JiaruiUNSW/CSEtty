# Sensor Window Anomalies — solution

## Approach

Enumerate every valid start index, compute that window's extrema and range, update the global maximum, and count ranges meeting the inclusive threshold.

## Correctness

Each possible fixed-width window is examined once and its helper range is exact. Counting qualifying exact ranges and taking their maximum gives both requested statistics.

## Complexity

O((n - width + 1) * width) time and O(n) space.

## Common pitfalls

Use at least rather than greater than for the threshold, include the final start index, and initialise extrema from a value inside each window. Verify boundary inputs as well as the worked example.

