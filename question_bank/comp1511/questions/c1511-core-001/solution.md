# Count Echo Valleys — solution

## Approach

Read the sequence, then visit each interior index and increment a counter exactly when both strict less-than comparisons succeed.

## Correctness

For every possible interior index, the loop checks precisely the two inequalities in the definition. It increments once for each valley and never for a non-valley, so the final counter is exact.

## Complexity

The scan takes O(n) time and the stored array uses O(n) space.

## Common pitfalls

Do not inspect outside the array, count endpoints, or treat equal adjacent values as a strict valley. Also check every `scanf` target and preserve the required output format.

