# Solution: Find the first signed decimal

## Approach

Scan for either a digit or a sign followed by a digit. Record the sign, then accumulate consecutive digit values and store the signed result.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_022 abc -42x`.

Input:

```text
(empty)
```

Expected standard output:

```text
-42
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every position before the selected start is rejected by the exact token-start predicate. At the selected start the loop consumes exactly its digit run and computes its positional decimal value, so the first valid token is returned.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Accepting a bare sign, skipping the digit after rejecting a sign, using `isdigit` on a negative plain `char`, or relying on prohibited conversion functions. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
