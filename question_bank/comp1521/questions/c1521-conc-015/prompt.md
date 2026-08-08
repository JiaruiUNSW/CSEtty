# Indexed Pipe Worker Farm

## Background

A worker farm completes tasks out of order. Carrying a task index in every result lets the parent reconstruct deterministic input order.

## Requirements

- Write `c1521_conc_015.c`.
- Invocation is `./c1521_conc_015 WORKERS VALUE ...`, with 1 to 4 workers, 1 to 16 values, and each value -100 through 100.
- Create one task pipe per worker and one shared result pipe.
- Fork all workers.
- Send task (i), containing index and value, to worker `i % WORKERS`; then send an explicit stop record to every worker.
- A worker computes signed square and cube and writes one complete result record to the shared pipe.
- Parent reads exactly one result per task, stores by validated unique index, reaps all children, and prints index, original value, square, and cube in input order.
- Print each task as `INDEX value=V square=S cube=C`.

## Examples

Command:

```text
./c1521_conc_015 2 2 -3 4
```

Output:

```text
0 value=2 square=4 cube=8
1 value=-3 square=9 cube=-27
2 value=4 square=16 cube=64
```

## Implementation notes

Keep each result record smaller than `PIPE_BUF` and issue it with one successful `write`, so records from different workers cannot interleave. Task pipes have one writer and reader; complete-transfer helpers are still required there. Close every worker's unrelated task descriptors and all unused result ends. Validate duplicate/out-of-range result indices. Submit `c1521_conc_015.c`.
