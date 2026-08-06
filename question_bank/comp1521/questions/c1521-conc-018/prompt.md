# Parallel Integer Frequency Merge

## Background

Several file-reading threads can build private frequency tables and merge them under a mutex. Local accumulation minimizes shared critical-section time.

## Requirements

Implement `c1521_conc_018.c` with one to six file arguments. Create one thread per file. Each worker opens its own file, parses whitespace-separated decimal integers in the inclusive range -10 through 10, and accumulates a private 21-entry histogram. At EOF it locks a shared mutex once, adds its local table and value count into the global state, and unlocks. Malformed/out-of-range input marks that job failed. Main joins all workers, then prints nonzero values in numeric order as `VALUE=COUNT`, followed by `values=TOTAL`.

## Examples

Files containing `-1 0 1 1` and `1 2 -1` combine to counts two for -1, one for 0, three for 1, and one for 2.

## Implementation notes

The worker owns its `FILE *`; no stdio stream is shared. Use a stable job array and per-job failure flag. The merge and total update form one mutex critical section. Join all successfully created threads even after a later creation failure, and destroy the mutex. Submit `c1521_conc_018.c`.
