# Worked solution

## Approach

Traverse the list and increment a counter for values within the inclusive ASCII digit range.

## Correctness

Each node is examined once and contributes exactly when its value is one of the ten digit characters.

## Complexity

Time is `O(n)` and extra space is `O(1)`.

## Common pitfalls

Converting the whole string to an integer, forgetting `0` or `9`, or modifying/freeing the caller's list.

