# Balanced Cut Counter — solution

## Approach

First sum all weights. Sweep possible cuts while adding the new leftmost item to a prefix sum; compare that prefix with total minus prefix.

## Correctness

At cut k, the prefix is exactly the sum of elements before the cut and total minus prefix is exactly the suffix. Thus the comparison accepts exactly balanced cuts.

## Complexity

Two linear passes take O(n) time and the input array takes O(n) space.

## Common pitfalls

There are n - 1 cuts, not n. Check the cut only after adding its left-side element. Also check every `scanf` target and preserve the required output format.

