# Solution: Clamp and count

## Approach

Visit each element through the array pointer. Replace values below low or above high and increment the counter only in those cases.

## Correctness

Each element is independently mapped to low, itself, or high according to its relation to the bounds. These are exactly the clamp cases, and the counter increments exactly for the two cases that alter the value.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Counting boundary values as changes, using mutually independent `if` statements with invalid bounds, or returning the sum rather than count. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
