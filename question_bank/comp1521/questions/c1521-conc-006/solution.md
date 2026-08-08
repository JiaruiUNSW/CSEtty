# Sharded Manifest Statistics solution

## Approach

Create one channel per worker, then fork. Each child closes unrelated descriptors, opens the file with `fopen`, and enumerates lines using `getline`. It analyses only line numbers in its congruence class, removes one final newline from the byte count, counts word starts, and sends a record. The parent reads records by index, waits for the matching PIDs, prints indexed values, and accumulates totals.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `two-workers`, runs `./c1521_conc_006 manifest.txt 2`.
The test installs `tests/two_lines.txt -> manifest.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
worker 0 lines=1 bytes=9 words=2
worker 1 lines=1 bytes=4 words=1
total lines=2 bytes=13 words=3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Modulo classes partition all nonnegative line numbers: every line belongs to exactly one worker. That worker adds the line once and computes its byte/word values from the specified content. Therefore adding all worker records gives the statistics of the full file. Parent-side index ordering produces deterministic output regardless of worker completion.

## Complexity

Although each of (W) workers scans the full file, total work is (O(WB)), bounded by (W\le8); each child stores one line and the parent stores (O(W)) records. This deliberately emphasizes ownership rather than optimal I/O.

## Common pitfalls

Sharing one inherited `FILE *` causes buffering and offset surprises. The newline is excluded from bytes but still separates words. Idle workers must report zeros, all write ends must be closed, and every PID must be reaped.
