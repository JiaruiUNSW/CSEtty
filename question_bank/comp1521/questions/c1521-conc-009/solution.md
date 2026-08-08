# Pipe Sequence Reduction solution

## Approach

Parse the three integers before forking. The child loops COUNT times, computes each arithmetic-sequence value, and sends it with a complete-write helper. The parent uses a complete-read helper exactly COUNT times, initializing min/max from the first value, updates all aggregates, then performs one byte read to require EOF and reaps the child.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `ascending`, runs `./c1521_conc_009 1 1 5`.

Input:

```text
(empty)
```

Expected standard output:

```text
count=5 sum=15 min=1 max=5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The child emits one record for each index in the specified range and in increasing index order. Complete transfers preserve every record. The parent applies standard sum, minimum, and maximum updates to all and only those COUNT values, so the final aggregates match the sequence. EOF and successful wait ensure no hidden extra output or producer failure.

## Complexity

Time and pipe traffic are (O(N)) for COUNT (N), while both processes use (O(1)) auxiliary memory.

## Common pitfalls

Treating a pipe as message-oriented loses partial records. Initializing minimum to zero fails for all-positive sequences. Waiting before reading could deadlock for larger streams, and retaining a writer prevents the EOF check.
