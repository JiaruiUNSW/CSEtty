# Classify a Binary32 Encoding — solution guide

## Approach

Branch on exponent zero, exponent 255, or an intermediate exponent. Within each special exponent, distinguish a zero fraction from a nonzero fraction.

## Correctness

IEEE-754 defines zero/subnormal for exponent zero, infinity/NaN for exponent all ones, and normal for every intermediate exponent. Fraction zero selects the first class in each special pair.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Do not cast or evaluate the bits as a host float; classification is a bit-field task. Negative zero is still `zero`.
