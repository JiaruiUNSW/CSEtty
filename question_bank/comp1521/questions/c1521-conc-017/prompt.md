# Bounded Square Queue

## Background

A bounded producer/consumer queue requires two conditions: consumers wait while it is empty, and the producer waits while it is full. A completion flag distinguishes temporary emptiness from end-of-input.

## Requirements

- Implement `c1521_conc_017.c` as `./c1521_conc_017 CAPACITY CONSUMERS VALUE ...`.
- CAPACITY is 1 through 8, CONSUMERS is 1 through 4, there are 1 through 16 values, and values are -10000 through 10000.
- Create one producer thread and the requested consumer threads.
- The producer enqueues indexed tasks in argument order into a circular queue protected by one mutex and `not_empty`/`not_full` condition variables, then sets `done` and broadcasts.
- Consumers dequeue until done and empty, compute squares, and store into the result slot named by the task index.
- Join all threads, print indexed squares in argument order, then `total=S`.
- Print each result as `INDEX square=S`, then print the final line `total=T`.

## Examples

Command:

```text
./c1521_conc_017 1 1 2 -3
```

Output:

```text
0 square=4
1 square=9
total=13
```

## Implementation notes

Every condition wait must be inside a `while` loop because wakeups may be spurious. Change queue count/head/tail and done only while holding the mutex. Signal `not_full` after dequeue and `not_empty` after enqueue. Result indices are unique, so separate slots need no mutex. Do not use sleeps or assume fairness. Submit `c1521_conc_017.c`.
