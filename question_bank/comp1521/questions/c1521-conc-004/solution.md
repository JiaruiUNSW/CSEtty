# Parallel Chunk Checksum solution

## Approach

After validating the worker count and file type, calculate all half-open chunks using integer division. Fork one child per chunk. A child opens the same path independently, walks its absolute range with `pread`, and accumulates additive statistics in a result record. The parent reads one record per dedicated channel, waits for all children, rejects failures, and sums the records.

## Correctness

The chunk formula partitions offsets from zero through size minus one: chunks do not overlap and their union is the whole file. Each child therefore counts every byte in its chunk once. Its weighted term uses the original absolute offset. Since count, sum, and weighted sum are additive over disjoint sets, combining all records equals a sequential scan. Output is one aggregate line, so completion order is irrelevant.

## Complexity

The total work and I/O are (O(B)) for (B) bytes, with (O(W)) descriptors and records for (W\le8) workers. Each child uses a fixed buffer.

## Common pitfalls

Using `read` on a descriptor inherited with a shared open-file description can race on the offset; independent opens plus `pread` avoid that. Chunk-relative weights change the answer. Zero-length chunks, partial pipe transfers, and failed child statuses still require correct handling.

