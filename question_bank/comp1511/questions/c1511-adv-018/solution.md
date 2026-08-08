# Solution: Clamp and count

## Approach

Visit each element through the array pointer. Replace values below low or above high and increment the counter only in those cases.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_018 0 10 -2 5 12`.

Input:

```text
(empty)
```

Expected standard output:

```text
changes=2
0 5 10
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each element is independently mapped to low, itself, or high according to its relation to the bounds. These are exactly the clamp cases, and the counter increments exactly for the two cases that alter the value.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Counting boundary values as changes, using mutually independent `if` statements with invalid bounds, or returning the sum rather than count. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
