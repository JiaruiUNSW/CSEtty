# Temperature Drift — solution

## Approach

Calculate end minus start once, select a direction from its sign, and print both fields.

## Correctness

The difference formula gives the required signed change. Positive, negative, and zero are exhaustive and mutually exclusive, so the selected direction is correct.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Preserve the sign by subtracting start from end, and spell the three labels exactly. Keep the submitted filename and required output format unchanged.

