# Worked solution — Q9

## Approach

In `sum_range`, cast the argument to `struct task *`, reset its sum, and add each
integer in the inclusive `[first, last]` interval. In `main`, check every create
and join return code, then add the two stored partial sums.

## Correctness

Each worker's loop visits every integer in its assigned inclusive interval
exactly once, so its stored value is that interval's sum. The supplied intervals
are disjoint and their union is `1..n`. Both joins finish before the values are
read. Adding the two partial sums therefore equals the sum of every integer from
1 through n exactly once.

## Complexity

Across both workers, time is O(n), with up to roughly n/2 additions on either
thread. Extra space is O(1).

## Common pitfalls

- Treating `last` as exclusive.
- Passing both threads the same mutable task object.
- Reading partial results before joining.
- Ignoring `pthread_create` and `pthread_join` failures.

