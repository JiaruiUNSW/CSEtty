# Three-Process Run Encoder solution

## Approach

Fork the reader to copy blocks from the opened file into pipe one. Fork the encoder to consume bytes, maintaining `have`, current byte, and current count; on change it writes the previous run, and at EOF writes the final run. Parent uses an EOF-aware complete-record reader, appends records dynamically, accumulates totals, then validates both wait statuses before any output.

## Correctness

The reader preserves file byte order. The encoder begins a run at the first byte, extends it exactly while following bytes match, and emits when the next byte differs or EOF arrives. Thus emitted records are precisely all maximal equal-byte runs, in file order, covering every byte once. Parent buffering preserves this order and sums record lengths to the file byte count.

## Complexity

For (B) bytes and (R) runs, time is (O(B+R)), pipeline traffic is (O(B+R)), and the parent stores (O(R)) records.

## Common pitfalls

Omitting the EOF flush loses the last run. Printing before child status checks exposes partial reports. Inherited raw-pipe writers prevent encoder EOF, and assuming one read equals one padded C structure can corrupt records.
