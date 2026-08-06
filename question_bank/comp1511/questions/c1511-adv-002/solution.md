# Solution: Record-high counter

## Approach

Handle the empty case, then keep the greatest value seen and a counter initialized for the first node. Increase both when a later value is strictly greater.

## Correctness

The stored maximum is the greatest value in the visited prefix. Therefore a new node is counted exactly when it exceeds every earlier node. Induction over the traversal proves the final counter equals the number of record highs.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Counting ties, initializing the maximum to zero instead of the first value, or dereferencing an empty head. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
