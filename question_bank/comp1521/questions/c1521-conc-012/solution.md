# Mutex Letter Histogram solution

## Approach

Store the shared counters and mutex in one context referenced by each job. A worker scans its assigned immutable string. On each ASCII letter, it derives index zero through 25, locks, increments that one counter, and unlocks. Main joins all threads, then reads the stable array in index order and destroys the mutex.

## Correctness

Every input letter causes exactly one protected increment of its corresponding shared counter; nonletters cause none. Mutual exclusion prevents two increments from losing one another, so after all joins each counter equals the total occurrences across all strings. Alphabetical main-thread traversal gives deterministic output.

## Complexity

For (C) total characters, work is (O(C)), shared storage is (O(1)), and thread metadata is (O(N)). Lock contention can serialize frequent letters but is bounded by the input.

## Common pitfalls

An unprotected `counts[index]++` is a data race. Forgetting an unlock can deadlock all remaining workers. Locale-sensitive classification on negative signed chars is undefined, and worker-side printing creates nondeterministic order.
