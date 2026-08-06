# Indexed Pipe Worker Farm

## Background

A worker farm completes tasks out of order. Carrying a task index in every result lets the parent reconstruct deterministic input order.

## Requirements

Write `c1521_conc_015.c`. Invocation is `./c1521_conc_015 WORKERS VALUE ...`, with 1 to 4 workers, 1 to 16 values, and each value -100 through 100. Create one task pipe per worker and one shared result pipe. Fork all workers. Send task (i), containing index and value, to worker `i % WORKERS`; then send an explicit stop record to every worker. A worker computes signed square and cube and writes one complete result record to the shared pipe. Parent reads exactly one result per task, stores by validated unique index, reaps all children, and prints index, original value, square, and cube in input order.

## Examples

Two workers given `2 -3 4` may return in any order, but output must be lines 0, 1, 2 with squares 4, 9, 16 and cubes 8, -27, 64.

## Implementation notes

Keep each result record smaller than `PIPE_BUF` and issue it with one successful `write`, so records from different workers cannot interleave. Task pipes have one writer and reader; complete-transfer helpers are still required there. Close every worker's unrelated task descriptors and all unused result ends. Validate duplicate/out-of-range result indices. Submit `c1521_conc_015.c`.
