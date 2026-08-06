# Concurrent File Fingerprints solution

## Approach

Allocate one pipe and PID slot per argument, then fork each worker. The child closes unrelated descriptors, scans its file in blocks, accumulates an unsigned byte count and modulo-65536 checksum, and writes one record. The parent reads records into index-matched slots, waits for each PID, validates statuses, and finally prints the array in input order.

## Correctness

Every file has exactly one worker and every byte returned by `read` is added once as an unsigned value. Reducing after each addition preserves the required modulo checksum. Dedicated pipes prevent record mixing. Since output is deferred and indexed by argv position, scheduler order cannot change the result.

## Complexity

For total bytes (B) across (F) files, total work is (O(B)), parent memory is (O(F)), and each child uses a fixed-size buffer. At most four workers exist.

## Common pitfalls

A signed `char` gives incorrect checksums for bytes above 127. Printing from children can reorder lines. Failing to close duplicate writers can obscure failure/EOF, and not reaping all children leaks zombies.

