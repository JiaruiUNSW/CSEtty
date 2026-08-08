# Solution: Record-high counter

## Approach

Handle the empty case, then keep the greatest value seen and a counter initialized for the first node. Increase both when a later value is strictly greater.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_002 3 1 4 4 7`.

Input:

```text
(empty)
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The stored maximum is the greatest value in the visited prefix. Therefore a new node is counted exactly when it exceeds every earlier node. Induction over the traversal proves the final counter equals the number of record highs.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Counting ties, initializing the maximum to zero instead of the first value, or dereferencing an empty head. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
