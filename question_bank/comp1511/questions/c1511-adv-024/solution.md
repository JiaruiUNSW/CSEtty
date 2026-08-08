# Solution: Append a dynamic checksum

## Approach

Compute the sum first, request space for one additional integer into a temporary pointer, then append the sum and publish the new pointer and length.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_024 1 2 3`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 2 3 6
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The sum covers exactly the original length. On allocation failure the caller state is unchanged. On success all old values are preserved by `realloc`, the checksum occupies the new final slot, and both outputs describe the grown array.

## Complexity

`O(n)` time and `O(1)` auxiliary space aside from allocator movement.

## Common pitfalls

Assigning `realloc` directly to the only pointer, incrementing length before success, or summing the new uninitialized slot. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
