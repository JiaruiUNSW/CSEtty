# Threaded Byte Histogram Merge solution

## Approach

Use `fstat` to size a regular file, allocate that many bytes, and fill it with a complete read loop. Build worker records with half-open slices. A worker zeroes its local histogram, scans its slice, then locks once to add local counters to the shared array. Main joins all workers and traverses byte values zero through 255 for output.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `aba`, runs `./c1521_conc_016 input.bin 2`.
The test installs `tests/aba.bin -> input.bin` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
0A=1
41=2
42=1
total=4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The slice formula partitions every file offset exactly once. Therefore the local histograms collectively count each byte once. Mutual exclusion makes each whole merge race-free, so the global counter for byte (b) becomes the sum of all local counts of (b), equal to its file frequency. Numeric traversal and post-join printing make output deterministic.

## Complexity

For file size (B) and thread count (T\le8), work is (O(B+256T)), storage is (O(B+256T)), and each worker acquires the mutex once.

## Common pitfalls

Using `strlen` truncates at NUL. Sharing one local histogram between threads races. Reading global counters before joins is unsafe, and locking once per byte creates unnecessary contention.
