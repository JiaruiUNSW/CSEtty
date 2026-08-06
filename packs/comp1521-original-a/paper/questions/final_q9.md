# Q9 — Sum a range with two POSIX threads

## Background

The supplied program partitions the inclusive range `1..n` into two disjoint
tasks. Each worker receives a pointer to its own `struct task`, computes one
partial sum, and stores the result in that object. The main thread joins both
workers before reading their results.

## Program requirements

Complete `final_q9.c` for positive `n` values whose sum fits in `long`.

- Implement `sum_range` so it sums every integer from `first` through `last`,
  inclusive, into `task->sum`.
- Create exactly two POSIX threads using the supplied task partition.
- Join both threads before printing the combined sum.
- Print only the decimal total and a newline.
- Treat a `pthread_create` or `pthread_join` failure as an error and return
  non-zero rather than using an incomplete result.

Do not introduce global shared state, detach either worker, create additional
threads, or replace the threaded computation with the closed-form formula.

## Examples

```text
$ ./final_q9 10
55
$ ./final_q9 100
5050
```

## Implementation notes

The two workers write to different `struct task` objects, so no mutex is needed.
The successful `pthread_join` operations establish that both writes are
complete before `main` reads them.

