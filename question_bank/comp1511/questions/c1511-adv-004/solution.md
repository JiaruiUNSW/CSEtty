# Solution: Longest rising-or-level run

## Approach

Scan left to right. Start a new run at one when the current value is below the previous value; otherwise extend the current run. Update the maximum after each node.

## Correctness

The current counter is the exact length of the nondecreasing run ending at the current node. The best counter is the maximum over all completed run endings. Thus after the last node it is the longest qualifying run.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Computing a subsequence, treating equality as a break, or returning one for an empty list. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
