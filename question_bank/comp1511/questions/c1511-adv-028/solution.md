# Solution: Recursive reverse copy

## Approach

Recursively traverse forward while allocating a copy of the current node and pushing it onto an accumulator head. Return the accumulator at the end.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_028 1 2 3`.

Input:

```text
(empty)
```

Expected standard output:

```text
3 2 1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After processing k input nodes, the accumulator is a deep copy of exactly those k nodes in reverse order. Prepending the next copied value preserves this invariant, so exhaustion returns the complete reversed copy.

## Complexity

`O(n)` time, `O(n)` returned heap space, and `O(n)` call-stack space.

## Common pitfalls

Returning original nodes, appending recursively in quadratic time, or sharing a next pointer between the lists. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
