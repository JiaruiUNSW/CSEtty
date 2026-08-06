# Solution: Append a dynamic checksum

## Approach

Compute the sum first, request space for one additional integer into a temporary pointer, then append the sum and publish the new pointer and length.

## Correctness

The sum covers exactly the original length. On allocation failure the caller state is unchanged. On success all old values are preserved by `realloc`, the checksum occupies the new final slot, and both outputs describe the grown array.

## Complexity

`O(n)` time and `O(1)` auxiliary space aside from allocator movement.

## Common pitfalls

Assigning `realloc` directly to the only pointer, incrementing length before success, or summing the new uninitialized slot. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
