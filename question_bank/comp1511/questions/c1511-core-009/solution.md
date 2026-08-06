# Strictly Rising Columns — solution

## Approach

For each column, compare each row after the first with the row above; return false on a less-than-or-equal pair and true if the scan finishes.

## Correctness

A column is strictly rising exactly when all adjacent comparisons are strict increases. The helper checks all and only those comparisons, so its answer is exact.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Equal neighbours invalidate strict increase. Handle one-row input without accessing row one. Also check every `scanf` target and preserve the required output format.

