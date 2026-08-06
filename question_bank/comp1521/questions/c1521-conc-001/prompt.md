# Forked File Totals

## Background

A parent process can delegate independent file scans to children and receive compact results through pipes. This task models a small batch-analysis tool without relying on scheduling order.

## Requirements

Write `c1521_conc_001.c`. The program is invoked as `./c1521_conc_001 FILE_A FILE_B`. Create exactly one child for each file and one pipe per child. Each child must open its own file, parse signed decimal integers separated by ASCII whitespace, and send a fixed-size result containing the value count, sum, and success status. The parent must close every unused pipe end, collect both results, call `waitpid` for both recorded PIDs, and print results in argument order as `INDEX count=N sum=S`. Return 1 with a useful diagnostic if a file, pipe, fork, read, write, or child operation fails.

## Examples

If the first file contains `1 2 3` and the second contains `10 20`, print:

```text
0 count=3 sum=6
1 count=2 sum=30
```

An empty file has count and sum zero.

## Implementation notes

Use POSIX `open`/`read` in the children and retry interrupted pipe reads or writes. Do not share a `FILE *` stream across `fork`. A child owns its file descriptor and pipe write end; the parent owns the corresponding pipe read end. Check signed 64-bit parsing and sum overflow assumptions: all supplied values and sums fit in `long long`. Submit only `c1521_conc_001.c`.

