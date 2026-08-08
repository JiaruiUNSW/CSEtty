# Compass Quarter Turns — solution

## Approach

Convert the direction to an enum index, add the signed turns, normalise into zero through three, and map that enum back to a character.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `clockwise`, runs `./c1511_core_022`.

Input:

```text
N 1
```

Expected standard output:

```text
direction: E
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Consecutive enum values encode clockwise quarter turns, so addition performs the rotation. Modulo four identifies equivalent full rotations, and normalisation selects the unique valid direction.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

C remainder may be negative. The clockwise order must be N, E, S, W. Keep the submitted filename and required output format unchanged.
