# Solution: Rotate a heap array left

## Approach

Reduce the amount modulo length. Reverse the prefix to rotate, reverse the suffix, then reverse the whole array.

## Correctness

The first two reversals reverse each of the two blocks independently. Reversing their concatenation restores each block's internal order while swapping the block order, exactly a left rotation.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Taking modulo when length is zero, using the unreduced amount, or reversing with an unsigned index that underflows. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
