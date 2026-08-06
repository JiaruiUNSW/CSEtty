# Absolute Sensor Gap — solution guide

## Approach

Subtract `b` from `a`. Test the sign of the result; negate it only when it is negative, then print it.

## Correctness

If `a-b` is non-negative, it equals `|a-b|`. If it is negative, its negation equals `b-a`, which is `|a-b|`. The branch selects exactly these two cases.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Reversing the subtraction happens to pass some cases but not all. Use a signed sign test and respect the stated range rather than attempting to handle `INT_MIN`.
