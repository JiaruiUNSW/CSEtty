# Solution: Deal nodes into two chains

## Approach

Initialize two empty output chains. Detach input nodes in order and append each to the tail link selected by an alternating index.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_027 1 2 3 4 5`.

Input:

```text
(empty)
```

Expected standard output:

```text
A: 1 3 5
B: 2 4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every input node is detached once and appended to the output matching its original parity. Tail appends preserve encounter order, so the two completed chains have exactly the required nodes and are properly terminated.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Leaving original cross-links intact, advancing after overwriting `next`, or forgetting to initialize empty outputs. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
