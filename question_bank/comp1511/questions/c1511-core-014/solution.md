# Descending Number Fence — solution

## Approach

Loop from n down through one, print the current value, and print `>` only when the current value is greater than one.

## Correctness

The loop visits every integer from n to one exactly once in descending order. Its separator condition is true precisely between consecutive outputs, so formatting is exact.

## Complexity

O(n) time and O(1) space.

## Common pitfalls

Avoid a trailing separator and remember the final newline. The case n equals one still prints one value. Keep the submitted filename and required output format unchanged.

