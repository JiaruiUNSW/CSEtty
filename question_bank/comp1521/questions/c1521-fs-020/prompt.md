# Lookup a fixed-width record

## Background

Fixed-width files support direct record access: record `i` begins at `i * width`, so reading earlier records is unnecessary.

## Requirements

Write `c1521_fs_020.c`. The file consists entirely of six-byte records: five data bytes followed by newline. Given `FILE INDEX`, where `INDEX` is non-negative decimal, use one positioned read to obtain that record and print its five data bytes plus newline. If the index is beyond the complete records, print `NOT FOUND`. A non-regular file, malformed file length or record newline, invalid index, overflow, or I/O failure prints `c1521_fs_020: error\n` to standard error and returns 1.

## Examples

A file containing `alpha\nbravo\n` returns `bravo` for index 1 and `NOT FOUND` for index 2.

## Implementation notes

Use `open`, `fstat`, `pread`, and `close`; do not scan preceding records or use `lseek` plus shared descriptor position. Check multiplication before converting the offset. Submit `c1521_fs_020.c`.
