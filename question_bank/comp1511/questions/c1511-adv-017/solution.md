# Solution: Order the endpoint values

## Approach

Compare the two dereferenced endpoint pointers and use one temporary integer to exchange them when out of order.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_017 9 2 4`.

Input:

```text
(empty)
```

Expected standard output:

```text
4 2 9
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

If the first endpoint is no greater, the required order already holds and nothing changes. Otherwise swapping places the smaller endpoint first and larger endpoint last while leaving all interior locations untouched.

## Complexity

`O(1)` time and `O(1)` space.

## Common pitfalls

Swapping pointer variables instead of pointed-to values, touching a one-element array, or always swapping. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
