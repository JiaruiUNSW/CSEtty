# Distance-Weighted Supply Chain — worked solution

## Idea in one sentence

Traverse the chain in order and maintain the minimal state for distance-weighted supply chain.

## Exact rule

Compute `sum((position + 1) * value)` in list order.

## Approach

Traverse the chain in order and maintain the minimal state for distance-weighted supply chain. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Handle `head == NULL` using the documented neutral result.
2. Save any current/next values needed by the metric before advancing.
3. Update the running result exactly once per eligible node or adjacent pair.
4. Return the scalar result; leave allocation and printing to the harness.

## Worked example

Command arguments: `3 -1 -1 4 0 -2`

Input:

```text
(empty)
```

Output:

```text
result: 2
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

After each traversal step, the accumulator equals the required metric for the consumed prefix. The update adds exactly the current node's or pair's contribution, and termination occurs after the final node, so the returned value is exact.

## Complexity

The list is traversed in `O(n)` time with `O(1)` iterative state. Recursive variants use `O(n)` call-stack space.

## Common pitfalls

Do not dereference `NULL`, advance twice, prefer the last maximum when the first is required, or free nodes inside the metric. An empty argument list is a real test case.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
