# Solution: Collapse sign regions

## Approach

For each region leader, accumulate and remove consecutive successors with the same sign class, then store the total in the leader and continue at the next region.

## Correctness

The inner loop consumes exactly the maximal same-class suffix after a leader. Its sum plus the leader gives that entire region's total. Repeating partitions and converts every region once without reordering.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Treating zero as its own class, failing to reconnect after a free, or advancing past an unprocessed region. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
