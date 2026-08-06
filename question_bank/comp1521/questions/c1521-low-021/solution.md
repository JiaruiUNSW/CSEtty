# Interleave Two Coordinate Words — solution guide

## Approach

Initialise the result to zero. For each bit index, extract the matching bit of `x` and `y`, then OR them into result positions `2i` and `2i+1`.

## Correctness

Each iteration writes exactly the two output positions assigned to one input index, and no two iterations overlap. After all 16 indices, every output bit has the specified source.

## Complexity

O(16), hence O(1), time and O(1) storage.

## Common pitfalls

Do not place `y` in the even positions. Shift unsigned values, and promote to `uint32_t` before moving a bit as high as position 31.
