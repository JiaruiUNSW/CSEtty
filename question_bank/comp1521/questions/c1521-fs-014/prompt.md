# Sorted directory inventory

## Background

`readdir` does not promise alphabetical order. Reproducible tools must inspect metadata, retain the desired records, and sort before reporting.

## Requirements

Write `c1521_fs_014.c`. Given one directory, report each immediate regular file as `NAME SIZE`, one per line, in bytewise `strcmp` order by name. Include names beginning with a dot except `.` and `..`; ignore subdirectories and symbolic links. Use `lstat` on the full child path. Wrong arguments or any `opendir`, `readdir`, metadata, allocation, or close failure prints `c1521_fs_014: error\n` to standard error and returns 1 without a successful report.

## Examples

If `z.bin` has two bytes and `a.txt` has three, output is `a.txt 3` then `z.bin 2` regardless of creation order.

## Implementation notes

Do not change working directory, recurse, follow symlinks, or invoke `ls`/`find`. Paths and entry names may be long, so allocate joined paths safely. Submit `c1521_fs_014.c`.
