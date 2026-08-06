# Two-Stage Word Pipeline solution

## Approach

Create both pipes before forking. The producer scans blocks, maintaining the current word length; at each whitespace transition it writes the completed positive length and finally writes any trailing word plus a zero sentinel. The aggregator reads lengths until zero, updates three aggregates, and sends a success-tagged structure. Parent reads, waits for both exact PIDs, and prints only on complete success.

## Correctness

The producer increments length once for each non-whitespace byte and emits exactly at word boundaries, so emitted positive records correspond one-to-one with input words and equal their lengths. The aggregator counts those records, sums them, and keeps their maximum. The sentinel is not aggregated. Thus the final structure contains precisely the specified statistics.

## Complexity

The file is scanned once in (O(B)) time; pipe traffic is (O(W)) records for (W) words. Every stage uses (O(1)) auxiliary storage.

## Common pitfalls

Not emitting the final unterminated word loses data. Closing the wrong inherited end can deadlock the pipeline. The parent must reap both stages, and structure/length transfers can be partial even though the records are small.
