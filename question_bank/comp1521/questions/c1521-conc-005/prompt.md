# Child-Built Line Index

## Background

A line index records the byte offset at which each logical line starts. A worker process can scan the file while the parent owns presentation and memory management.

## Requirements

Write `c1521_conc_005.c`, invoked with exactly one file. Create one pipe and one child. The child opens and scans the file byte by byte or in blocks and sends each existing line-start offset as an unsigned 64-bit value. Offset zero is sent only for a non-empty file; after a newline, the following offset is sent only if another byte actually exists. The parent reads until pipe EOF, stores offsets in a dynamically grown array, waits for the exact child, then prints `lines=N` followed by `LINE:OFFSET` lines numbered from 1. Failures return 1.

## Examples

The bytes `alpha\nbeta\n` have starts 0 and 6; there is no empty third line. The bytes `\n\nx` have starts 0, 1, and 2. An empty file prints only `lines=0`.

## Implementation notes

The child owns the input descriptor and pipe writer. The parent must close its writer before reading to EOF. Preserve offsets as `uint64_t`, handle partial pipe reads carefully, use `realloc` safely, and `waitpid` before accepting the result. Submit `c1521_conc_005.c`.

