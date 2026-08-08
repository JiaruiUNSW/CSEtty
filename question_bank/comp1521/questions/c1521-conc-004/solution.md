# Parallel Chunk Checksum solution

## Approach

After validating the worker count and file type, calculate all half-open chunks using integer division. Fork one child per chunk. A child opens the same path independently, walks its absolute range with `pread`, and accumulates additive statistics in a result record. The parent reads one record per dedicated channel, waits for all children, rejects failures, and sums the records.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `three-bytes-one-worker`, runs `./c1521_conc_004 data.bin 1`.
The test installs `tests/abc.bin -> data.bin` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
bytes=4 sum=208 weighted=438
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The chunk formula partitions offsets from zero through size minus one: chunks do not overlap and their union is the whole file. Each child therefore counts every byte in its chunk once. Its weighted term uses the original absolute offset. Since count, sum, and weighted sum are additive over disjoint sets, combining all records equals a sequential scan. Output is one aggregate line, so completion order is irrelevant.

## Complexity

The total work and I/O are (O(B)) for (B) bytes, with (O(W)) descriptors and records for (W\le8) workers. Each child uses a fixed buffer.

## Common pitfalls

Using `read` on a descriptor inherited with a shared open-file description can race on the offset; independent opens plus `pread` avoid that. Chunk-relative weights change the answer. Zero-length chunks, partial pipe transfers, and failed child statuses still require correct handling.
