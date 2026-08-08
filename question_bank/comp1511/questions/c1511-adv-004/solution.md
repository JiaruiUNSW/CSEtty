# Solution: Longest rising-or-level run

## Approach

Scan left to right. Start a new run at one when the current value is below the previous value; otherwise extend the current run. Update the maximum after each node.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_004 3 3 5 2 4`.

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

The current counter is the exact length of the nondecreasing run ending at the current node. The best counter is the maximum over all completed run endings. Thus after the last node it is the longest qualifying run.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Computing a subsequence, treating equality as a break, or returning one for an empty list. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
