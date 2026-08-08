# Mutex Letter Histogram solution

## Approach

Store the shared counters and mutex in one context referenced by each job. A worker scans its assigned immutable string. On each ASCII letter, it derives index zero through 25, locks, increments that one counter, and unlocks. Main joins all threads, then reads the stable array in index order and destroys the mutex.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `overlap`, runs `./c1521_conc_012 abc Baa`.

Input:

```text
(empty)
```

Expected standard output:

```text
a=3
b=2
c=1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every input letter causes exactly one protected increment of its corresponding shared counter; nonletters cause none. Mutual exclusion prevents two increments from losing one another, so after all joins each counter equals the total occurrences across all strings. Alphabetical main-thread traversal gives deterministic output.

## Complexity

For (C) total characters, work is (O(C)), shared storage is (O(1)), and thread metadata is (O(N)). Lock contention can serialize frequent letters but is bounded by the input.

## Common pitfalls

An unprotected `counts[index]++` is a data race. Forgetting an unlock can deadlock all remaining workers. Locale-sensitive classification on negative signed chars is undefined, and worker-side printing creates nondeterministic order.
