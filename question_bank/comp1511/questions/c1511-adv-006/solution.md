# Solution: Remove the first debt

## Approach

Use a pointer to the link that currently names each node. When it names a negative node, redirect that link to the successor, free the removed node, and return.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_006 2 -3 4`.

Input:

```text
(empty)
```

Expected standard output:

```text
2 4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Before removal, the link pointer has passed only nonnegative nodes, so the first negative encountered is the first in list order. Redirecting exactly its incoming link preserves every other node and makes the correct new head when needed.

## Complexity

`O(n)` worst-case time and `O(1)` space.

## Common pitfalls

Forgetting the head case, continuing and deleting multiple nodes, or accessing the node after freeing it. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
