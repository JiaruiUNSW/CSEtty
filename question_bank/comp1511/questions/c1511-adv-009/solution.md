# Solution: Bridge adjacent values

## Approach

At each original left node, save its original successor, allocate the sum node, insert it, then advance directly to the saved successor.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_009 1 2 3`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 3 2 5 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each iteration handles exactly one original adjacency and advances to the next original node, so no inserted edge is reconsidered. The bridge value is the endpoint sum and all original order is retained.

## Complexity

`O(n)` time and `O(n)` newly allocated space in the worst case.

## Common pitfalls

Advancing into the new node and inserting forever, overwriting the original successor, or omitting allocation checks. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
