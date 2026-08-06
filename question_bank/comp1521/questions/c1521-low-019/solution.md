# Rotate a 32-Bit Word — solution guide

## Approach

Return the input when the count is zero; otherwise OR the left-shifted body with the high bits wrapped down by the complementary shift.

## Correctness

Every original bit moves `k` positions modulo 32: bits that remain in range come from the left shift, and wrapped bits come from the right shift. The disjoint pieces OR to the rotation.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Signed right shift is implementation-defined for negatives. Never evaluate `value >> 32` in the zero-count case.
