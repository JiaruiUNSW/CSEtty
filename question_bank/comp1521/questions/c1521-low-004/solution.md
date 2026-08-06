# Largest of Three — solution guide

## Approach

Maintain a `maximum` register. Two signed `slt` comparisons decide whether the second and third inputs replace it.

## Correctness

After considering each input, the candidate is the maximum of the values seen so far. Applying this invariant to all three inputs leaves the maximum of the complete set.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Unsigned comparison gives incorrect answers for negative inputs. Avoid a control-flow path that skips reading or considering the third value.
