# Joined Range Sum

## Background

Threads share an address space, but a parent thread should not consume a worker's result until `pthread_join` establishes completion.

## Requirements

Implement `c1521_conc_010.c` as `./c1521_conc_010 N THREADS`, where (0\le N\le1,000,000) and THREADS is 1 through 8. Create exactly THREADS workers. Worker (i) owns integers from `N*i/THREADS + 1` through `N*(i+1)/THREADS`, inclusive; an empty range contributes zero. Each worker writes only its own result slot and returns. The main thread joins every successfully created worker, adds partial sums only after joins, and prints `sum=S`. Check parsing and pthread return codes.

## Examples

For N=10 and two threads, ranges are 1..5 and 6..10, so the printed sum is 55. More threads than values is valid.

## Implementation notes

Pass each thread a stable argument object rather than the address of a changing loop variable. No mutex is required because result slots are disjoint and read after join. On partial creation failure, join already-created threads before returning 1. Submit `c1521_conc_010.c`.
