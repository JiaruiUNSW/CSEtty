# Solution: Copy values inside a gate

## Approach

First count values satisfying both inclusive bounds. Allocate exactly that many integers, then scan again and copy qualifying values in order.

## Correctness

The count pass yields the exact result length. The second pass copies precisely each qualifying input once in encounter order, so the allocated result has the required contents and size.

## Complexity

`O(n)` time, `O(k)` returned space for k qualifying values, and `O(1)` other space.

## Common pitfalls

Using exclusive bounds, allocating zero bytes and treating its implementation-defined result as data, or failing to write the output length. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
