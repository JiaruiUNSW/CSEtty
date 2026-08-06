# Diagonal Colour Changes — solution

## Approach

Walk diagonal indices from one to n - 1 and compare grid[i][i] with grid[i - 1][i - 1], counting inequalities.

## Correctness

Every consecutive pair on the main diagonal corresponds to exactly one loop index, and the loop counts it exactly when its values differ. Therefore all and only changes are counted.

## Complexity

Reading uses O(n squared) time and space; the diagonal scan itself is O(n).

## Common pitfalls

Do not compare values in the same row or anti-diagonal, and do not count the first diagonal value as a change. Also check every `scanf` target and preserve the required output format.

