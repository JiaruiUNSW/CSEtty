# Solution: Distance between first extremes

## Approach

Track the first minimum and maximum indices while scanning. Update only on a strict new extreme, then subtract the smaller final index from the larger.

## Correctness

Strict updates maintain each index as the earliest location of the extreme in the visited prefix. At the end they are the specified global locations, and their absolute index difference is returned.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Updating on equality, subtracting unsigned indices in the wrong order, or reading element zero for an empty array. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
