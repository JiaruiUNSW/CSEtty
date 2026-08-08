# Solution: Allocate the vowel trace

## Approach

Use a helper predicate, count qualifying bytes, allocate count plus one, then copy the same qualifying bytes and append the terminator.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_020 Granite`.

Input:

```text
(empty)
```

Expected standard output:

```text
aie
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The count makes room for every and only vowel plus the terminator. The second traversal appends vowels in encounter order, so the result is precisely the required subsequence.

## Complexity

`O(n)` time and `O(v)` returned space for v vowels.

## Common pitfalls

Forgetting uppercase vowels, omitting the null terminator, or returning a pointer into the immutable input. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
