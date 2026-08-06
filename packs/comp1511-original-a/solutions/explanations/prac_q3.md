# Worked solution

## Approach

Walk a pointer-to-pointer until it designates the first negative node or `NULL`. Relink through that pointer, save the removed node, and free it.

## Correctness

All earlier nodes are non-negative by the loop condition. If a node is removed, the incoming link is redirected to its successor, preserving every other node and their order.

## Complexity

Time is `O(n)` and extra space is `O(1)`.

## Common pitfalls

Forgetting the head case, freeing before reading `next`, deleting every negative node, or leaking the removed node.

