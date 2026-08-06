# Unique Column Beacons — solution

## Approach

Scan each column from top to bottom, tracking the largest value and how many times it occurs, then count the column if the occurrence count is one.

## Correctness

After each row, the tracked value is the maximum of the visited prefix and the count is its exact multiplicity. At column end, count one therefore means precisely a unique maximum.

## Complexity

O(rows * columns) time and O(rows * columns) grid storage.

## Common pitfalls

When finding a new larger value, reset the occurrence count. Equal maxima must increase it. Also check every `scanf` target and preserve the required output format.

