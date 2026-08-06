# Parcel Classifier — solution

## Approach

Read a parcel struct, compute its volume, then use the precedence order oversized, compact, standard to return a classification string.

## Correctness

The first condition covers every oversized rule. If it is false, the compact condition covers exactly the eligible remaining parcels; all unclassified parcels must therefore be standard.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Use strict greater-than for oversized limits and less-than-or-equal for compact limits. Respect the stated precedence. Keep the submitted filename and required output format unchanged.

