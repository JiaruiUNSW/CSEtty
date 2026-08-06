# Sharded Manifest Statistics solution

## Approach

Create one channel per worker, then fork. Each child closes unrelated descriptors, opens the file with `fopen`, and enumerates lines using `getline`. It analyses only line numbers in its congruence class, removes one final newline from the byte count, counts word starts, and sends a record. The parent reads records by index, waits for the matching PIDs, prints indexed values, and accumulates totals.

## Correctness

Modulo classes partition all nonnegative line numbers: every line belongs to exactly one worker. That worker adds the line once and computes its byte/word values from the specified content. Therefore adding all worker records gives the statistics of the full file. Parent-side index ordering produces deterministic output regardless of worker completion.

## Complexity

Although each of (W) workers scans the full file, total work is (O(WB)), bounded by (W\le8); each child stores one line and the parent stores (O(W)) records. This deliberately emphasizes ownership rather than optimal I/O.

## Common pitfalls

Sharing one inherited `FILE *` causes buffering and offset surprises. The newline is excluded from bytes but still separates words. Idle workers must report zeros, all write ends must be closed, and every PID must be reaped.

