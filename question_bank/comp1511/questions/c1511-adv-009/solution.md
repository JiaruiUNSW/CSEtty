# Solution: Bridge adjacent values

## Approach

At each original left node, save its original successor, allocate the sum node, insert it, then advance directly to the saved successor.

## Correctness

Each iteration handles exactly one original adjacency and advances to the next original node, so no inserted edge is reconsidered. The bridge value is the endpoint sum and all original order is retained.

## Complexity

`O(n)` time and `O(n)` newly allocated space in the worst case.

## Common pitfalls

Advancing into the new node and inserting forever, overwriting the original successor, or omitting allocation checks. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
