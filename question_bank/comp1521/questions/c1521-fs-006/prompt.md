# Measure fixed binary records

## Background

Fixed-width binary formats divide file length by a record size. A partial suffix often signals an interrupted or incompatible write and must be reported rather than silently counted as a record.

## Requirements

Write `c1521_fs_006.c`. Run it as `./c1521_fs_006 FILE RECORD_SIZE`, where `RECORD_SIZE` is a positive decimal integer. Use metadata to print `records=R trailing=T`, where `R` is the number of complete records and `T` is the remaining byte count. The filename must identify a regular file. Invalid input or failed metadata lookup prints `c1521_fs_006: error\n` to standard error and returns 1.

## Examples

An eight-byte file measured with record size 3 prints `records=2 trailing=2`. With record size 4 it prints two complete records and zero trailing bytes.

## Implementation notes

Use `stat`; do not read the file contents or invoke `wc`. Preserve the full range of `off_t` when doing division and formatting. Submit `c1521_fs_006.c`.
