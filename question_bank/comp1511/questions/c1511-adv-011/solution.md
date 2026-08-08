# Solution: Outside-in weave

## Approach

Find the end of the first half with slow/fast pointers, detach and reverse the second half, then alternately link one node from each half.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_011 1 2 3 4 5`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 5 2 4 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The split gives the front half in ascending original positions and the reversed back half in descending positions. Alternating them emits first, last, second, second-last until the back half is exhausted; the remaining middle node is already linked last.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Choosing the wrong midpoint for even lengths, forgetting to detach before reversal, or creating a cycle during weaving. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
