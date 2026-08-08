# Solution: Unique merge of two sorted arrays

## Approach

Repeatedly choose the smaller current value, advancing both sides on equality. Append the chosen value only when it differs from the last emitted value.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_016 1 3 5 -- 2 3 4`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 2 3 4 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At every step the chosen value is the smallest unprocessed value from either sorted input. Skipping equality and repeated emitted values removes all duplicates. Exhaustion therefore leaves every distinct input value exactly once in sorted order.

## Complexity

`O(n + m)` time and `O(n + m)` maximum returned space.

## Common pitfalls

Advancing only one side when values are equal, forgetting duplicates within one input, or reading past an exhausted array. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
