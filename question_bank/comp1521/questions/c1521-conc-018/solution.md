# Parallel Integer Frequency Merge solution

## Approach

Each job carries one path and a shared-state pointer. The worker zeroes a stack histogram, repeatedly uses `fscanf` to parse integers, rejects invalid tokens/ranges, then locks and adds all 21 cells plus its local total. Main joins, checks every job, traverses value indices from -10 to 10, and prints the global total.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `two-files`, runs `./c1521_conc_018 a.txt b.txt`.
The test installs `tests/a.txt -> a.txt, tests/b.txt -> b.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
-1=2
0=1
1=3
2=1
values=7
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Worker (i) scans exactly file (i), incrementing its local cell once per valid input integer. Files are disjoint sources, so summing all local tables gives the combined frequencies. The mutex serializes entire merges, preventing lost updates. After joins the global table is stable, and ascending index traversal provides deterministic output.

## Complexity

For (N) total integers and (F\le6) files, work is (O(N+21F)), storage is (O(F)) jobs plus constant-size local/global histograms.

## Common pitfalls

Sharing a `FILE *` across threads is unnecessary and unsafe. Updating the global table without locking loses increments. `fscanf` returning zero indicates malformed input rather than EOF, and printing from workers scrambles order.
