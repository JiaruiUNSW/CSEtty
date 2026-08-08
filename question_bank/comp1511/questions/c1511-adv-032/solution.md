# Solution: Recursive even-prefix filter

## Approach

Add the current value and save the parity decision. Recursively filter the suffix using the shared running sum. Link and return the current node if saved as even; otherwise free it and return the filtered suffix.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_032 1 1 2 3 1`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 2 1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The shared sum at each call entry is the prefix before that node, so after addition the saved decision exactly matches its inclusive original prefix. Induction supplies the correct suffix, and the keep/free branch produces the correct filtered list.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Testing parity after returning from recursion, excluding removed values from later prefix sums, or accessing a freed current node. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
