# Three-Process Run Encoder solution

## Approach

Fork the reader to copy blocks from the opened file into pipe one. Fork the encoder to consume bytes, maintaining `have`, current byte, and current count; on change it writes the previous run, and at EOF writes the final run. Parent uses an EOF-aware complete-record reader, appends records dynamically, accumulates totals, then validates both wait statuses before any output.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `grouped`, runs `./c1521_conc_019 input.bin`.
The test installs `tests/grouped.bin -> input.bin` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
61 3
62 2
63 1
0A 1
runs=4 bytes=7
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The reader preserves file byte order. The encoder begins a run at the first byte, extends it exactly while following bytes match, and emits when the next byte differs or EOF arrives. Thus emitted records are precisely all maximal equal-byte runs, in file order, covering every byte once. Parent buffering preserves this order and sums record lengths to the file byte count.

## Complexity

For (B) bytes and (R) runs, time is (O(B+R)), pipeline traffic is (O(B+R)), and the parent stores (O(R)) records.

## Common pitfalls

Omitting the EOF flush loses the last run. Printing before child status checks exposes partial reports. Inherited raw-pipe writers prevent encoder EOF, and assuming one read equals one padded C structure can corrupt records.
