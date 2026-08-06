# Compass Quarter Turns — solution

## Approach

Convert the direction to an enum index, add the signed turns, normalise into zero through three, and map that enum back to a character.

## Correctness

Consecutive enum values encode clockwise quarter turns, so addition performs the rotation. Modulo four identifies equivalent full rotations, and normalisation selects the unique valid direction.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

C remainder may be negative. The clockwise order must be N, E, S, W. Keep the submitted filename and required output format unchanged.

