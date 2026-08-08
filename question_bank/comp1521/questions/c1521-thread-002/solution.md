# Threaded Positive Count — worked solution

## Idea in one sentence

Partition indices by residue modulo three and merge local values for threaded positive count under a mutex.

## Exact rule

Count input elements strictly greater than zero; zero does not count.

## Approach

Partition indices by residue modulo three and merge local values for threaded positive count under a mutex. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Read the array before creating threads.
2. Create three stable jobs with distinct start indices.
3. Compute each local result without shared writes, then lock once to merge.
4. Join every thread before printing and destroying the mutex.

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

The three residue classes are disjoint and cover every array index. Each worker computes the exact metric contribution of its class; mutex-serialised addition loses no contribution, so the joined total equals the full metric.

## Complexity

Total work is `O(n)`, shared storage is `O(n)`, and each worker locks once.

## Common pitfalls

Do not pass the address of a changing loop variable, print before joins, hold the mutex for the whole scan, or forget that empty classes are valid.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
