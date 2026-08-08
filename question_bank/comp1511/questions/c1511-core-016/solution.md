# Parcel Classifier — solution

## Approach

Read a parcel struct, compute its volume, then use the precedence order oversized, compact, standard to return a classification string.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `compact`, runs `./c1511_core_016`.

Input:

```text
4 10 10 8
```

Expected standard output:

```text
class: compact
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The first condition covers every oversized rule. If it is false, the compact condition covers exactly the eligible remaining parcels; all unclassified parcels must therefore be standard.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Use strict greater-than for oversized limits and less-than-or-equal for compact limits. Respect the stated precedence. Keep the submitted filename and required output format unchanged.
