# Solution: Alternating-position total

## Approach

Walk from the head while maintaining a zero-based index. Add a node's value exactly when the index is even.

## Correctness

At each iteration the accumulator equals the sum of all even-positioned nodes already visited. The next node is added precisely for an even index, so the invariant remains true. At list end every requested position has been visited, hence the returned total is correct.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Starting the index at one, advancing by two links without handling the final node, or modifying the list. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
