# Solution: Remove the first debt

## Approach

Use a pointer to the link that currently names each node. When it names a negative node, redirect that link to the successor, free the removed node, and return.

## Correctness

Before removal, the link pointer has passed only nonnegative nodes, so the first negative encountered is the first in list order. Redirecting exactly its incoming link preserves every other node and makes the correct new head when needed.

## Complexity

`O(n)` worst-case time and `O(1)` space.

## Common pitfalls

Forgetting the head case, continuing and deleting multiple nodes, or accessing the node after freeing it. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
