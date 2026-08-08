# Solution: Copy values inside a gate

## Approach

First count values satisfying both inclusive bounds. Allocate exactly that many integers, then scan again and copy qualifying values in order.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_015 2 5 1 2 5 7`.

Input:

```text
(empty)
```

Expected standard output:

```text
2 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The count pass yields the exact result length. The second pass copies precisely each qualifying input once in encounter order, so the allocated result has the required contents and size.

## Complexity

`O(n)` time, `O(k)` returned space for k qualifying values, and `O(1)` other space.

## Common pitfalls

Using exclusive bounds, allocating zero bytes and treating its implementation-defined result as data, or failing to write the output length. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
