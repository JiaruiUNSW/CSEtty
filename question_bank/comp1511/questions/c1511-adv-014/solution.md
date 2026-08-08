# Solution: Compact neighbouring repeats

## Approach

If nonempty, retain the first value and scan each later value. Copy it to the next write position only when it differs from the last retained value.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_014 1 1 2 2 2 3`.

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

After every read step, the written prefix contains exactly one representative for every complete run seen so far. A changed value starts a new run and is copied; an equal value belongs to the current run and is skipped.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Comparing against the previous unread element after overwriting, returning the original length, or reading element zero for empty input. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
