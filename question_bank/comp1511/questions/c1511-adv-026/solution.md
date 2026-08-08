# Solution: Recursive threshold pruning

## Approach

Obtain the filtered suffix recursively. If the current node is below threshold, free it and return the suffix; otherwise connect it to the suffix and return it.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_026 3 1 3 5 2`.

Input:

```text
(empty)
```

Expected standard output:

```text
3 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

By induction the recursive result contains exactly qualifying suffix nodes in order. The current node is prepended exactly when it qualifies; otherwise freeing it and returning the suffix gives precisely the filtered current list.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Using a freed node's next pointer, forgetting to assign the filtered suffix, or leaking a rejected head. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
