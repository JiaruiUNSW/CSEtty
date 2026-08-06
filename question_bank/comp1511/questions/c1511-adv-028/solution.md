# Solution: Recursive reverse copy

## Approach

Recursively traverse forward while allocating a copy of the current node and pushing it onto an accumulator head. Return the accumulator at the end.

## Correctness

After processing k input nodes, the accumulator is a deep copy of exactly those k nodes in reverse order. Prepending the next copied value preserves this invariant, so exhaustion returns the complete reversed copy.

## Complexity

`O(n)` time, `O(n)` returned heap space, and `O(n)` call-stack space.

## Common pitfalls

Returning original nodes, appending recursively in quadratic time, or sharing a next pointer between the lists. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
