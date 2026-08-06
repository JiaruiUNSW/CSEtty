# Cyclic Trail Distance — solution

## Approach

For every index i, select `(i + 1) % n`, add the absolute label difference, and return the accumulated sum.

## Correctness

Each of the n trail edges begins at exactly one index i and ends at its modulo successor. The loop adds each defined edge cost exactly once, hence returns the required total.

## Complexity

O(n) time and O(n) space for the input array.

## Common pitfalls

Do not omit the closing edge, and take the absolute difference rather than a signed difference. Also check every `scanf` target and preserve the required output format.

