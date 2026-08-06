# Solution: Order the endpoint values

## Approach

Compare the two dereferenced endpoint pointers and use one temporary integer to exchange them when out of order.

## Correctness

If the first endpoint is no greater, the required order already holds and nothing changes. Otherwise swapping places the smaller endpoint first and larger endpoint last while leaving all interior locations untouched.

## Complexity

`O(1)` time and `O(1)` space.

## Common pitfalls

Swapping pointer variables instead of pointed-to values, touching a one-element array, or always swapping. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
