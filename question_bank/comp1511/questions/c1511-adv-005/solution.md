# Solution: Insert after the last even node

## Approach

Traverse once while remembering the last even node. Allocate the new node after the scan. Link it after the remembered node, or make it the new head when no even node exists.

## Correctness

The remembered pointer is updated for every even node, so at traversal end it is exactly the last even node. Linking after it gives the requested position; if it is null, the specification requires front insertion. No other links change.

## Complexity

`O(n)` time and `O(1)` auxiliary space, plus one allocated node.

## Common pitfalls

Stopping at the first even node, losing the successor link, or failing on an empty list. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
