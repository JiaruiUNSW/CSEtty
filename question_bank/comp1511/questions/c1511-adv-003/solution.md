# Solution: First prefix threshold

## Approach

Accumulate a `long` prefix sum while tracking the node index. Return immediately on the first prefix meeting the threshold; return -1 after exhaustion.

## Correctness

Before each comparison, the accumulator is exactly the inclusive sum through the current node. Traversal order is increasing index, so the first successful comparison is the smallest qualifying index. If none succeeds, no prefix qualifies.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Checking before adding the current value, assuming monotone sums, or returning a one-based position. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
