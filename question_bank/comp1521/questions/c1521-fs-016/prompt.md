# Largest immediate file

## Background

Selecting an extremum from directory metadata requires a deterministic tie rule because directory iteration order is unspecified.

## Requirements

Write `c1521_fs_016.c`. Examine immediate children of the directory argument with `lstat`, ignoring directories, symlinks, and other types. Print `NAME SIZE` for the largest regular file. If several have the same size, select the bytewise lexicographically smallest name. If none exist, print `NONE`. Any operational failure prints `c1521_fs_016: error\n` to standard error and returns 1.

## Examples

For equal three-byte files `zeta` and `alpha`, output is `alpha 3` even if `zeta` is returned first.

## Implementation notes

Use `opendir`, `readdir`, and `lstat`. Include ordinary dotfiles, skip only `.` and `..`, do not recurse, and do not invoke shell utilities. Submit `c1521_fs_016.c`.
