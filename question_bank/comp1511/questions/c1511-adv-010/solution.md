# Solution: Collapse sign regions

## Approach

For each region leader, accumulate and remove consecutive successors with the same sign class, then store the total in the leader and continue at the next region.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_010 2 -1 -3 4 5`.

Input:

```text
(empty)
```

Expected standard output:

```text
2 -4 9
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The inner loop consumes exactly the maximal same-class suffix after a leader. Its sum plus the leader gives that entire region's total. Repeating partitions and converts every region once without reordering.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Treating zero as its own class, failing to reconnect after a free, or advancing past an unprocessed region. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
