# Solution: Keep first occurrences

## Approach

For each surviving node, scan the suffix through a pointer-to-pointer and unlink every later node with the same value.

## Correctness

After processing a node, no later equal node remains. Earlier processed values likewise have no later duplicates. Induction leaves one node—the earliest—for every distinct value, in original order.

## Complexity

`O(n^2)` time and `O(1)` auxiliary space.

## Common pitfalls

Advancing the link after deletion, retaining the last occurrence instead of the first, or leaking removed nodes. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
