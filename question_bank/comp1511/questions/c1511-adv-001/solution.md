# Solution: Alternating-position total

## Approach

Walk from the head while maintaining a zero-based index. Add a node's value exactly when the index is even.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_001 4 7 1 9`.

Input:

```text
(empty)
```

Expected standard output:

```text
5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At each iteration the accumulator equals the sum of all even-positioned nodes already visited. The next node is added precisely for an even index, so the invariant remains true. At list end every requested position has been visited, hence the returned total is correct.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Starting the index at one, advancing by two links without handling the final node, or modifying the list. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
