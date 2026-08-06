# Triangle Label — solution

## Approach

Reject if any inequality fails, otherwise test all-three equality, then any pair equality, and use scalene as the remaining case.

## Correctness

The rejection predicate is exactly the negation of the strict triangle inequalities. Among valid triangles, the ordered equality tests partition cases into three equal, exactly two equal, and none equal.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

A sum equal to the third side is invalid. Check every side ordering and test invalidity before equality labels. Keep the submitted filename and required output format unchanged.

