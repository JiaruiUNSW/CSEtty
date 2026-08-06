# Solution: Repair the frequency allocation

## Approach

Allocate `maximum + 1` `size_t` counters with `calloc`, check the result, then increment the counter indexed by each input value.

## Correctness

Zero initialisation establishes all counts for an empty prefix. Each input increments exactly its key's counter, preserving the invariant that every cell equals occurrences in the processed prefix.

## Complexity

`O(maximum + n)` allocator/processing time and `O(maximum)` returned space.

## Common pitfalls

Using uninitialised `malloc` storage, allocating bytes instead of elements times element size, or omitting key zero. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
