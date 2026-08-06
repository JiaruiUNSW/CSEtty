# Worked solution

## Approach

Save `*left`, assign `*right` into `*left`, then assign the saved value into `*right`.

## Correctness

The temporary preserves the original left value while the two destination objects are overwritten, leaving each with the other's original value.

## Complexity

Time and extra space are `O(1)`.

## Common pitfalls

Swapping local pointer addresses, omitting dereferences, or overwriting the first value before saving it.

