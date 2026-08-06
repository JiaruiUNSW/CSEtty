# Solution: Deal nodes into two chains

## Approach

Initialize two empty output chains. Detach input nodes in order and append each to the tail link selected by an alternating index.

## Correctness

Every input node is detached once and appended to the output matching its original parity. Tail appends preserve encounter order, so the two completed chains have exactly the required nodes and are properly terminated.

## Complexity

`O(n)` time and `O(1)` auxiliary space.

## Common pitfalls

Leaving original cross-links intact, advancing after overwriting `next`, or forgetting to initialize empty outputs. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
