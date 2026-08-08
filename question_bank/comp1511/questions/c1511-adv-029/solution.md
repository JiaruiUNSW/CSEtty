# Solution: Recursive mirror check

## Approach

Recursively reach the list end with a right pointer. During unwinding compare each right-side value with a shared front pointer, then advance that front pointer.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_029 1 2 1`.

Input:

```text
(empty)
```

Expected standard output:

```text
YES
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Unwinding visits right-side nodes from last to first while the shared pointer visits left-side nodes from first to last. Each symmetric pair is compared once; conjunction of all comparisons is true exactly for a palindrome.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Advancing the front pointer on the downward recursion, mutating the list, or continuing to dereference after an earlier mismatch. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
