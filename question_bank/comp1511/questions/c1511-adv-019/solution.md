# Solution: Repair running differences

## Approach

Save the original element zero. For each later index, save the current original, write current minus saved previous, then update the saved previous.

## Correctness

Before each iteration the saved value is the original predecessor. The assignment therefore writes the specified difference, and saving the current original before overwriting establishes the invariant for the next index.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Subtracting an already transformed predecessor, starting at index zero, or allocating an unnecessary copy. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
