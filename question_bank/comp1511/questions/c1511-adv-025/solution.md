# Solution: Recursive neighbouring totals

## Approach

For each call allocate a node holding either the first-two sum or the lone final value. Set its next pointer to the recursive result for the remaining suffix.

## Correctness

The base case produces the empty result. Each nonempty call creates exactly the required first result element and, by induction, links it to the correct result for all remaining pairs, yielding the full pair-total list.

## Complexity

`O(n)` time, `O(n)` returned heap space, and `O(n)` recursion stack.

## Common pitfalls

Advancing two nodes when only one remains, reusing input nodes despite the const interface, or freeing input inside the function. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
