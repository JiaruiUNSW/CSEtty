# Solution: Consume an alternating checksum

## Approach

Iterate with a sign that alternates between +1 and -1. Save the next link, update the total, free the current node, and advance.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_012 5 2 1`.

Input:

```text
(empty)
```

Expected standard output:

```text
4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At iteration k the total is the required alternating sum of the first k values, and those k nodes are freed. Processing the next node adds its correctly signed value and frees it. At termination the full checksum is returned and no nodes remain.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Reading `next` after `free`, applying the same sign twice, or freeing the list again in `main`. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
