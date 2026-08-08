# Solution: Alternating chain weave

## Approach

Maintain an output tail link. While both lists exist, detach and append one left node and one right node. Attach whichever source remains to the tail.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_030 1 3 5 -- 2 4`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 2 3 4 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each iteration appends the next unused node from each list in required order and preserves their internal orders. Once one source ends, the untouched remainder is exactly the required suffix.

## Complexity

`O(min(n,m))` explicit loop time and `O(1)` space; the returned list contains all `n+m` nodes.

## Common pitfalls

Losing a source successor, appending right first, creating a cycle, or attempting to free nodes still in the result. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
