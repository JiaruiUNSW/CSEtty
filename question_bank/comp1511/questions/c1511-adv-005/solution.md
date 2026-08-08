# Solution: Insert after the last even node

## Approach

Traverse once while remembering the last even node. Allocate the new node after the scan. Link it after the remembered node, or make it the new head when no even node exists.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_005 9 2 4 5`.

Input:

```text
(empty)
```

Expected standard output:

```text
2 4 9 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The remembered pointer is updated for every even node, so at traversal end it is exactly the last even node. Linking after it gives the requested position; if it is null, the specification requires front insertion. No other links change.

## Complexity

`O(n)` time and `O(1)` auxiliary space, plus one allocated node.

## Common pitfalls

Stopping at the first even node, losing the successor link, or failing on an empty list. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
