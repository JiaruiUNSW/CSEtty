# Solution: Consume an alternating checksum

## Approach

Iterate with a sign that alternates between +1 and -1. Save the next link, update the total, free the current node, and advance.

## Correctness

At iteration k the total is the required alternating sum of the first k values, and those k nodes are freed. Processing the next node adds its correctly signed value and frees it. At termination the full checksum is returned and no nodes remain.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Reading `next` after `free`, applying the same sign twice, or freeing the list again in `main`. Also keep the supplied input/output harness unchanged, check every allocation requested by the task, and respect whether the function owns or merely observes its input nodes.
