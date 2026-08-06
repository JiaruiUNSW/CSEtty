# Apply Set and Clear Masks — solution guide

## Approach

OR the original word with the set mask, complement the clear mask, then AND the two results.

## Correctness

OR forces every set-mask position to one. AND with the complemented clear mask then forces every clear-mask position to zero and preserves all remaining positions, matching the specified order.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Applying clear before set changes overlap semantics. A logical `!` is not the bitwise complement `~`.
