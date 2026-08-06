# Parallel Integer Frequency Merge solution

## Approach

Each job carries one path and a shared-state pointer. The worker zeroes a stack histogram, repeatedly uses `fscanf` to parse integers, rejects invalid tokens/ranges, then locks and adds all 21 cells plus its local total. Main joins, checks every job, traverses value indices from -10 to 10, and prints the global total.

## Correctness

Worker (i) scans exactly file (i), incrementing its local cell once per valid input integer. Files are disjoint sources, so summing all local tables gives the combined frequencies. The mutex serializes entire merges, preventing lost updates. After joins the global table is stable, and ascending index traversal provides deterministic output.

## Complexity

For (N) total integers and (F\le6) files, work is (O(N+21F)), storage is (O(F)) jobs plus constant-size local/global histograms.

## Common pitfalls

Sharing a `FILE *` across threads is unnecessary and unsafe. Updating the global table without locking loses increments. `fscanf` returning zero indicates malformed input rather than EOF, and printing from workers scrambles order.
