# Solution: Allocate the vowel trace

## Approach

Use a helper predicate, count qualifying bytes, allocate count plus one, then copy the same qualifying bytes and append the terminator.

## Correctness

The count makes room for every and only vowel plus the terminator. The second traversal appends vowels in encounter order, so the result is precisely the required subsequence.

## Complexity

`O(n)` time and `O(v)` returned space for v vowels.

## Common pitfalls

Forgetting uppercase vowels, omitting the null terminator, or returning a pointer into the immutable input. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
