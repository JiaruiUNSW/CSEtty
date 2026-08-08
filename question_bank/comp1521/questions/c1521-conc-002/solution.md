# Concurrent File Fingerprints solution

## Approach

Allocate one pipe and PID slot per argument, then fork each worker. The child closes unrelated descriptors, scans its file in blocks, accumulates an unsigned byte count and modulo-65536 checksum, and writes one record. The parent reads records into index-matched slots, waits for each PID, validates statuses, and finally prints the array in input order.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `ascii-pair`, runs `./c1521_conc_002 a.bin b.bin`.
The test installs `tests/a.bin -> a.bin, tests/b.bin -> b.bin` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
0 bytes=4 checksum=304
1 bytes=5 checksum=161
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every file has exactly one worker and every byte returned by `read` is added once as an unsigned value. Reducing after each addition preserves the required modulo checksum. Dedicated pipes prevent record mixing. Since output is deferred and indexed by argv position, scheduler order cannot change the result.

## Complexity

For total bytes (B) across (F) files, total work is (O(B)), parent memory is (O(F)), and each child uses a fixed-size buffer. At most four workers exist.

## Common pitfalls

A signed `char` gives incorrect checksums for bytes above 127. Printing from children can reorder lines. Failing to close duplicate writers can obscure failure/EOF, and not reaping all children leaks zombies.
