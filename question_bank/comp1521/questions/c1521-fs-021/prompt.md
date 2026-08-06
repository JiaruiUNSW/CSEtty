# Swap binary records in place

## Background

In-place binary updates require positioned reads and complete writes. Record bytes are arbitrary; they cannot be passed to string functions.

## Requirements

Write `c1521_fs_021.c`. Treat the regular file argument as consecutive four-byte records. Arguments two and three are valid non-negative record indices. Swap those records in place, then print the complete resulting file as continuous lowercase hexadecimal followed by newline. The same index is allowed and leaves data unchanged. Invalid size, index, arithmetic, or I/O prints `c1521_fs_021: error\n` to standard error and returns 1.

## Examples

Swapping the first two records of bytes `AAAABBBB` produces bytes `BBBBAAAA`, printed as `4242424241414141`.

## Implementation notes

Use `open` with read/write access, `fstat`, `pread`, and a loop around `pwrite`. Do not load the file solely to perform the swap; a later streaming read for hexadecimal reporting is allowed. Submit `c1521_fs_021.c`.
