# Saturating Signed Addition — solution guide

## Approach

Compute the wrapped unsigned sum. If both operands were non-negative and the result sign is one, return the maximum. If both were negative and the result sign is zero, return the minimum. Otherwise reinterpret the wrapped sum.

## Correctness

Two's-complement addition overflows exactly under the two sign-change cases tested. The selected bound is the required saturation direction; absent overflow, the 32-bit sum represents the mathematical result.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Evaluating `a+b` as signed C before checking is undefined on overflow. Opposite-sign operands cannot overflow and should not be clamped.
