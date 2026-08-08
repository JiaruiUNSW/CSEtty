# Solution: Stable odd-even relink

## Approach

Build two head/tail chains by detaching nodes one at a time. Append odd nodes to one chain and even nodes to the other, then join the odd tail to the even head.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_008 4 1 3 2`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 3 4 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Appending maintains original order within each parity chain. Every input node enters exactly one chain. Joining odd then even therefore produces precisely the stable partition.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Using `value % 2 == 1` for negative odds, losing the next pointer before detaching, or forming a cycle. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
