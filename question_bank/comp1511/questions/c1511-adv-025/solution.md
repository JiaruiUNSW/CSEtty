# Solution: Recursive neighbouring totals

## Approach

For each call allocate a node holding either the first-two sum or the lone final value. Set its next pointer to the recursive result for the remaining suffix.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_025 1 2 3 4 5`.

Input:

```text
(empty)
```

Expected standard output:

```text
3 7 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The base case produces the empty result. Each nonempty call creates exactly the required first result element and, by induction, links it to the correct result for all remaining pairs, yielding the full pair-total list.

## Complexity

`O(n)` time, `O(n)` returned heap space, and `O(n)` recursion stack.

## Common pitfalls

Advancing two nodes when only one remains, reusing input nodes despite the const interface, or freeing input inside the function. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
