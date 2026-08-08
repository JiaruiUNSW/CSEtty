# Solution: Distance between first extremes

## Approach

Track the first minimum and maximum indices while scanning. Update only on a strict new extreme, then subtract the smaller final index from the larger.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_021 4 1 7 1 7`.

Input:

```text
(empty)
```

Expected standard output:

```text
1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Strict updates maintain each index as the earliest location of the extreme in the visited prefix. At the end they are the specified global locations, and their absolute index difference is returned.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Updating on equality, subtracting unsigned indices in the wrong order, or reading element zero for an empty array. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
