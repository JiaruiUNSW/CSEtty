# Solution: Rotate a heap array left

## Approach

Reduce the amount modulo length. Reverse the prefix to rotate, reverse the suffix, then reverse the whole array.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_013 2 1 2 3 4 5`.

Input:

```text
(empty)
```

Expected standard output:

```text
3 4 5 1 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The first two reversals reverse each of the two blocks independently. Reversing their concatenation restores each block's internal order while swapping the block order, exactly a left rotation.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Taking modulo when length is zero, using the unreduced amount, or reversing with an unsigned index that underflows. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
