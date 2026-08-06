# Solution: Stable odd-even relink

## Approach

Build two head/tail chains by detaching nodes one at a time. Append odd nodes to one chain and even nodes to the other, then join the odd tail to the even head.

## Correctness

Appending maintains original order within each parity chain. Every input node enters exactly one chain. Joining odd then even therefore produces precisely the stable partition.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Using `value % 2 == 1` for negative odds, losing the next pointer before detaching, or forming a cycle. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
