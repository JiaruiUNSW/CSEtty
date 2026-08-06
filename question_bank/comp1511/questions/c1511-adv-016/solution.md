# Solution: Unique merge of two sorted arrays

## Approach

Repeatedly choose the smaller current value, advancing both sides on equality. Append the chosen value only when it differs from the last emitted value.

## Correctness

At every step the chosen value is the smallest unprocessed value from either sorted input. Skipping equality and repeated emitted values removes all duplicates. Exhaustion therefore leaves every distinct input value exactly once in sorted order.

## Complexity

`O(n + m)` time and `O(n + m)` maximum returned space.

## Common pitfalls

Advancing only one side when values are equal, forgetting duplicates within one input, or reading past an exhausted array. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
