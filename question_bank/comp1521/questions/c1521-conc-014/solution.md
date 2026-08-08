# Two-Stage Word Pipeline solution

## Approach

Create both pipes before forking. The producer scans blocks, maintaining the current word length; at each whitespace transition it writes the completed positive length and finally writes any trailing word plus a zero sentinel. The aggregator reads lengths until zero, updates three aggregates, and sends a success-tagged structure. Parent reads, waits for both exact PIDs, and prints only on complete success.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `three-words`, runs `./c1521_conc_014 input.txt`.
The test installs `tests/three.txt -> input.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
words=3 chars=11 longest=5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The producer increments length once for each non-whitespace byte and emits exactly at word boundaries, so emitted positive records correspond one-to-one with input words and equal their lengths. The aggregator counts those records, sums them, and keeps their maximum. The sentinel is not aggregated. Thus the final structure contains precisely the specified statistics.

## Complexity

The file is scanned once in (O(B)) time; pipe traffic is (O(W)) records for (W) words. Every stage uses (O(1)) auxiliary storage.

## Common pitfalls

Not emitting the final unterminated word loses data. Closing the wrong inherited end can deadlock the pipeline. The parent must reap both stages, and structure/length transfers can be partial even though the records are small.
