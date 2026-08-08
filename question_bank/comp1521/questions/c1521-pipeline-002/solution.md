# Pipe-Transferred Positive Count — worked solution

## Idea in one sentence

Compute pipe-transferred positive count in the child and use the pipe as the only result channel back to the parent.

## Exact rule

Count input elements strictly greater than zero; zero does not count.

## Approach

Compute pipe-transferred positive count in the child and use the pipe as the only result channel back to the parent. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Read all data before `fork` and create the pipe.
2. Close opposite pipe ends in parent and child.
3. Compute and write one fixed-size result, then `_exit(0)`.
4. Read the full record, wait for success, and print in the parent.

## Worked example

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
result: 2
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

The child applies the metric to the inherited immutable array and writes exactly that scalar. The parent prints only the complete record after confirming child success, so the observable result equals the specified reduction.

## Complexity

The child performs `O(n)` work; pipe traffic and extra storage are `O(1)` beyond the input array.

## Common pitfalls

Do not expect shared memory after `fork`, leave both writers open, accept a short read/write, call buffered `exit` in the child, or ignore child status.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
