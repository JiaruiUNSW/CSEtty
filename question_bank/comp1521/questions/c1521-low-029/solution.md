# Recursive Binary Search — solution guide

## Approach

Save call state in a frame, check the empty range, and inspect the midpoint. Return it on equality; otherwise update either `high` or `low` and recursively search that smaller interval.

## Correctness

If the midpoint differs from the target, strict ordering proves the target can occur only in the selected half. Each recursive range is smaller, and the empty range correctly represents absence, so the result is exactly the target index or -1.

## Complexity

O(log n) time and O(log n) stack space.

## Common pitfalls

Use signed comparisons because array values may be negative. An incorrect midpoint or unchanged bound causes infinite recursion; remember that even the not-found path must restore the frame.
