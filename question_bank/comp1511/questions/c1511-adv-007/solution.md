# Solution: Keep first occurrences

## Approach

For each surviving node, scan the suffix through a pointer-to-pointer and unlink every later node with the same value.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_007 1 2 1 3 2`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 2 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After processing a node, no later equal node remains. Earlier processed values likewise have no later duplicates. Induction leaves one node—the earliest—for every distinct value, in original order.

## Complexity

`O(n^2)` time and `O(1)` auxiliary space.

## Common pitfalls

Advancing the link after deletion, retaining the last occurrence instead of the first, or leaking removed nodes. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
