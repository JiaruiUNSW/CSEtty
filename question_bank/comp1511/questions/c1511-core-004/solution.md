# Balanced Cut Counter — solution

## Approach

First sum all weights. Sweep possible cuts while adding the new leftmost item to a prefix sum; compare that prefix with total minus prefix.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `uniform`, runs `./c1511_core_004`.

Input:

```text
4
1 1 1 1
```

Expected standard output:

```text
balanced cuts: 1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At cut k, the prefix is exactly the sum of elements before the cut and total minus prefix is exactly the suffix. Thus the comparison accepts exactly balanced cuts.

## Complexity

Two linear passes take O(n) time and the input array takes O(n) space.

## Common pitfalls

There are n - 1 cuts, not n. Check the cut only after adding its left-side element. Also check every `scanf` target and preserve the required output format.
