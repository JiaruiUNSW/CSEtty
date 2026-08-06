# Forked Threaded Parity Scan

## Background

Threads created after `fork` live only inside the child process. Their shared-memory result must be joined and then explicitly transferred through IPC before the parent can observe it.

## Requirements

Implement `c1521_conc_020.c` for one text file containing 1 to 1000 signed integers. Create one pipe and fork one child. The child opens/parses the file into owned memory, creates exactly three worker threads, and assigns indices `i, i+3, ...` to worker (i). Each worker computes local count, even/odd counts and sums, minimum, and maximum; it then locks one mutex and merges the entire local summary into child-shared state. The child joins all threads and sends one success-tagged summary to the parent. Parent reads it, waits for the child, and prints the specified fields in one line.

## Examples

For `1 2 3 4`, count is four; even count/sum are 2 and 6; odd count/sum are 2 and 4; minimum and maximum are 1 and 4.

## Implementation notes

The parent cannot read the child's mutex-protected memory directly because `fork` creates a separate address space. Merge min/max only from a local summary that has at least one value; zero is not a safe initial minimum. Close pipe ends, join all child threads, destroy the child mutex, use a complete structure transfer, and check `waitpid`. Submit `c1521_conc_020.c`.
