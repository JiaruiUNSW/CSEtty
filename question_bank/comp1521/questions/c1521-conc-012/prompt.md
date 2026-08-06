# Mutex Letter Histogram

## Background

Threads that update one shared histogram perform read-modify-write operations. A mutex makes each update critical section atomic with respect to other workers.

## Requirements

Write `c1521_conc_012.c`. Accept one to eight strings and create one thread per string. All workers share a 26-element counter array and one initialized `pthread_mutex_t`. For every ASCII letter, convert to lowercase, lock the mutex, increment that letter's counter, and unlock. Ignore other bytes. Join all workers, print only nonzero counters from `a` to `z` as `LETTER=N`, destroy the mutex, and return 0. Any pthread failure returns 1 after the safest possible cleanup.

## Examples

Inputs `abc` and `Baa` produce `a=3`, `b=2`, and `c=1`, one per line in alphabetic order.

## Implementation notes

The required critical section is intentionally explicit; a local histogram merged later would solve a different exercise. Keep the mutex locked for only one increment, never print while holding it, and use unsigned-byte character classification. Empty strings are valid. Submit `c1521_conc_012.c`.
