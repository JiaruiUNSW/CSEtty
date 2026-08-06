# Calm Grid Rows — solution

## Approach

For each row, scan its columns to obtain a minimum and maximum, compare their difference with the tolerance, and count successful rows.

## Correctness

The helper examines every value in a row, so its extrema and range are exact. The outer loop counts exactly those rows whose exact range meets the calm condition.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Negative values make zero a bad extrema sentinel. Use `<= tolerance`, not a strict comparison. Also check every `scanf` target and preserve the required output format.

