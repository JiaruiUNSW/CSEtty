# Forked Threaded Parity Scan solution

## Approach

After fork, the child parses integers into a dynamic array and initializes a shared summary plus mutex. Three stable job records point to the array with different starting indices and stride three. Each worker accumulates a local summary without locking, then locks once to add counts/sums and merge extrema. Child joins, destroys the mutex, writes a result record, and exits. Parent reads and validates that record and child status before printing.

## Correctness

Stride-three index sets are disjoint and cover every parsed index, so each integer appears in exactly one local summary. Each worker classifies parity, adds its value to the matching sum, and maintains local extrema. Mutex serialization makes all whole-summary merges lossless; additive fields combine exactly and extrema merge over all non-empty locals. The pipe is required because parent and child do not share post-fork writes.

## Complexity

For (N\le1000), parsing and threaded work are (O(N)), the child stores (O(N)) integers, and each of three workers acquires the mutex once. Pipe traffic is one fixed record.

## Common pitfalls

Creating threads before fork is outside this design and can leave mutex state unsafe. Assuming the parent sees child memory changes is incorrect. Initializing minimum to zero fails for positive-only input, and sending before joins exposes incomplete data.
