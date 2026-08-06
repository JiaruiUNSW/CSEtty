# Pipe Sequence Reduction solution

## Approach

Parse the three integers before forking. The child loops COUNT times, computes each arithmetic-sequence value, and sends it with a complete-write helper. The parent uses a complete-read helper exactly COUNT times, initializing min/max from the first value, updates all aggregates, then performs one byte read to require EOF and reaps the child.

## Correctness

The child emits one record for each index in the specified range and in increasing index order. Complete transfers preserve every record. The parent applies standard sum, minimum, and maximum updates to all and only those COUNT values, so the final aggregates match the sequence. EOF and successful wait ensure no hidden extra output or producer failure.

## Complexity

Time and pipe traffic are (O(N)) for COUNT (N), while both processes use (O(1)) auxiliary memory.

## Common pitfalls

Treating a pipe as message-oriented loses partial records. Initializing minimum to zero fails for all-positive sequences. Waiting before reading could deadlock for larger streams, and retaining a writer prevents the EOF check.
