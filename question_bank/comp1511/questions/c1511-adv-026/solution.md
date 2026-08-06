# Solution: Recursive threshold pruning

## Approach

Obtain the filtered suffix recursively. If the current node is below threshold, free it and return the suffix; otherwise connect it to the suffix and return it.

## Correctness

By induction the recursive result contains exactly qualifying suffix nodes in order. The current node is prepended exactly when it qualifies; otherwise freeing it and returning the suffix gives precisely the filtered current list.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Using a freed node's next pointer, forgetting to assign the filtered suffix, or leaking a rejected head. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
