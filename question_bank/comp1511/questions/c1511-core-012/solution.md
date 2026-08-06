# Shifted Signal Mismatches — solution

## Approach

For every B index i, calculate the corresponding rotated A index `(i + shift) % n`, compare the values, and count differences.

## Correctness

The formula selects exactly the element appearing at position i after the defined left rotation. Since all n positions are compared once, the mismatch count is exact.

## Complexity

O(n) time and O(n) space for the two input signals.

## Common pitfalls

Apply the shift in the stated direction, wrap with modulo, and compare with B at the unshifted index. Also check every `scanf` target and preserve the required output format.

