# Apply Set and Clear Masks — solution guide

## Approach

OR the original word with the set mask, complement the clear mask, then AND the two results.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `overlap`, runs `./c1521_low_018`.

Input:

```text
0000000a 00000005 00000008
```

Expected standard output:

```text
00000007
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

OR forces every set-mask position to one. AND with the complemented clear mask then forces every clear-mask position to zero and preserves all remaining positions, matching the specified order.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Applying clear before set changes overlap semantics. A logical `!` is not the bitwise complement `~`.
