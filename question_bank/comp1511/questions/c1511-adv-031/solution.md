# Solution: Repair the frequency allocation

## Approach

Allocate `maximum + 1` `size_t` counters with `calloc`, check the result, then increment the counter indexed by each input value.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_031 4 1 3 1`.

Input:

```text
(empty)
```

Expected standard output:

```text
1=2 3=1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Zero initialisation establishes all counts for an empty prefix. Each input increments exactly its key's counter, preserving the invariant that every cell equals occurrences in the processed prefix.

## Complexity

`O(maximum + n)` allocator/processing time and `O(maximum)` returned space.

## Common pitfalls

Using uninitialised `malloc` storage, allocating bytes instead of elements times element size, or omitting key zero. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
