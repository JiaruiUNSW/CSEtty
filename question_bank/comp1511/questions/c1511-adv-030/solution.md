# Solution: Alternating chain weave

## Approach

Maintain an output tail link. While both lists exist, detach and append one left node and one right node. Attach whichever source remains to the tail.

## Correctness

Each iteration appends the next unused node from each list in required order and preserves their internal orders. Once one source ends, the untouched remainder is exactly the required suffix.

## Complexity

`O(min(n,m))` explicit loop time and `O(1)` space; the returned list contains all `n+m` nodes.

## Common pitfalls

Losing a source successor, appending right first, creating a cycle, or attempting to free nodes still in the result. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
