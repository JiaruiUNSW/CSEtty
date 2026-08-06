# Solution: Recursive character tally

## Approach

Return zero at the terminator. Otherwise add whether the current byte equals the target to the recursive count of the suffix.

## Correctness

The base case correctly counts the empty suffix. Assuming recursion counts the suffix, adding the current byte's match indicator gives the exact count for the whole current string.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Recursing without advancing, counting the terminator, or comparing strings rather than individual characters. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
