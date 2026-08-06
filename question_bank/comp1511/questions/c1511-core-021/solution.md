# Alternating Digit Score — solution

## Approach

Repeatedly take value modulo ten, add or subtract it according to a toggled sign, then divide value by ten until no digits remain.

## Correctness

At iteration k, remainder extracts exactly the kth digit from the right and the toggled sign matches the alternating definition. Every digit is processed once.

## Complexity

O(D) time for D digits and O(1) space.

## Common pitfalls

The rightmost digit is added, not subtracted. Ensure input zero produces score zero. Keep the submitted filename and required output format unchanged.

