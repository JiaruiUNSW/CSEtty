# Forked Threaded Parity Scan solution

## Approach

After fork, the child parses integers into a dynamic array and initializes a shared summary plus mutex. Three stable job records point to the array with different starting indices and stride three. Each worker accumulates a local summary without locking, then locks once to add counts/sums and merge extrema. Child joins, destroys the mutex, writes a result record, and exits. Parent reads and validates that record and child status before printing.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `positive`, runs `./c1521_conc_020 input.txt`.
The test installs `tests/positive.txt -> input.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
count=4 even=2 even_sum=6 odd=2 odd_sum=4 min=1 max=4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Stride-three index sets are disjoint and cover every parsed index, so each integer appears in exactly one local summary. Each worker classifies parity, adds its value to the matching sum, and maintains local extrema. Mutex serialization makes all whole-summary merges lossless; additive fields combine exactly and extrema merge over all non-empty locals. The pipe is required because parent and child do not share post-fork writes.

## Complexity

For (N\le1000), parsing and threaded work are (O(N)), the child stores (O(N)) integers, and each of three workers acquires the mutex once. Pipe traffic is one fixed record.

## Common pitfalls

Creating threads before fork is outside this design and can leave mutex state unsafe. Assuming the parent sees child memory changes is incorrect. Initializing minimum to zero fails for positive-only input, and sending before joins exposes incomplete data.
