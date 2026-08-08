# Threaded Positive Count

## Background

Three worker threads process disjoint stride-three positions of a bounded sensor array. They merge local results under one mutex so output remains deterministic.

## Requirements

Read `n` and `n` integers. Create exactly three workers for indices `start, start+3, ...`, merge the title's metric, join all workers, and print `result: X`.

**Exact rule.** Count input elements strictly greater than zero; zero does not count.

Submit `c1521_thread_002.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
result: 2
```

## Implementation notes

Pass stable job records, compute locally before locking, check thread calls, and destroy the mutex after all joins.
