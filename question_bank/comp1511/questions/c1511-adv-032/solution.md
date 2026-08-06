# Solution: Recursive even-prefix filter

## Approach

Add the current value and save the parity decision. Recursively filter the suffix using the shared running sum. Link and return the current node if saved as even; otherwise free it and return the filtered suffix.

## Correctness

The shared sum at each call entry is the prefix before that node, so after addition the saved decision exactly matches its inclusive original prefix. Induction supplies the correct suffix, and the keep/free branch produces the correct filtered list.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Testing parity after returning from recursion, excluding removed values from later prefix sums, or accessing a freed current node. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
