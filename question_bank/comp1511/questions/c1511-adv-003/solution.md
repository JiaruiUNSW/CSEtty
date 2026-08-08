# Solution: First prefix threshold

## Approach

Accumulate a `long` prefix sum while tracking the node index. Return immediately on the first prefix meeting the threshold; return -1 after exhaustion.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_003 6 2 1 3`.

Input:

```text
(empty)
```

Expected standard output:

```text
2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Before each comparison, the accumulator is exactly the inclusive sum through the current node. Traversal order is increasing index, so the first successful comparison is the smallest qualifying index. If none succeeds, no prefix qualifies.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Checking before adding the current value, assuming monotone sums, or returning a one-based position. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
