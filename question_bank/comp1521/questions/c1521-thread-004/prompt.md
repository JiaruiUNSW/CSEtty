# Threaded Absolute Total

## Task

Return the sum of the absolute values of all input elements.

## Background

Three worker threads process disjoint stride-three positions of a bounded sensor array. They merge local results under one mutex so output remains deterministic.

## Requirements

Read `n` and `n` integers. The supplied `main` creates exactly three workers. Worker `start` processes indices `start, start + 3, ...`; each worker computes a local value, locks once to merge it, and returns. After all joins the program prints `result: X`.

## Starter code

Complete `static void *worker(void *arg)`. The supplied `main` reads the array, creates and joins exactly three threads, destroys the mutex, and prints the merged total.

## Examples

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
result: 11
```

## Implementation notes

Pass stable job records, compute locally before locking, check thread calls, and destroy the mutex after all joins.

## Submission

Submit `c1521_thread_004.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
