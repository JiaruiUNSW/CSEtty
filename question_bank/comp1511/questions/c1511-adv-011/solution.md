# Solution: Outside-in weave

## Approach

Find the end of the first half with slow/fast pointers, detach and reverse the second half, then alternately link one node from each half.

## Correctness

The split gives the front half in ascending original positions and the reversed back half in descending positions. Alternating them emits first, last, second, second-last until the back half is exhausted; the remaining middle node is already linked last.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Choosing the wrong midpoint for even lengths, forgetting to detach before reversal, or creating a cycle during weaving. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
