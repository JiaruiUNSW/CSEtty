# Summarise directory extensions

## Background

Grouping metadata requires both filename parsing and deterministic aggregation. This task defines extension syntax narrowly so dotfiles and trailing dots are unambiguous.

## Requirements

Write `c1521_fs_018.c`. Examine immediate regular files in a directory using `lstat`. An extension is the non-empty suffix after the last dot, only when that dot is not the first character; otherwise use `[none]`. For each extension print `EXT COUNT BYTES`, sorted by `strcmp` on `EXT`. Ignore directories and symlinks. Any error prints `c1521_fs_018: error\n` to standard error and returns 1.

## Examples

`a.tar.gz` and `b.gz` both belong to `gz`. `.env`, `README`, and `name.` belong to `[none]`.

## Implementation notes

Use dynamic storage for groups, compare extension strings exactly and case-sensitively, and add `st_size` values without reading contents. Do not recurse or invoke shell tools. Submit `c1521_fs_018.c`.
