# Recursive file manifest

## Background

A reproducible manifest uses root-relative names and global sorting, not the incidental order of nested directory reads.

## Requirements

- Write `c1521_fs_017.c`.
- Recursively traverse the directory argument without following symbolic links.
- Print every regular file as `RELATIVE_PATH SIZE`, where paths use `/`, omit the root prefix, and are globally sorted by bytewise `strcmp`.
- Include dot-named entries except `.` and `..`; ignore non-regular, non-directory objects.
- On any failure print `c1521_fs_017: error\n` to standard error and return 1 without a successful manifest.

## Examples

Command:

```text
./c1521_fs_017 tree
```

Files provided for this example:

- `tree/a.txt` (3 bytes) contains:

  ```text
  aa
  ```
- `tree/sub/b.txt` (4 bytes) contains:

  ```text
  bbb
  ```
- `tree/z.txt` (2 bytes) contains:

  ```text
  z
  ```

Output:

```text
a.txt 3
sub/b.txt 4
z.txt 2
```

## Implementation notes

Use `opendir`, `readdir`, `lstat`, dynamic path construction, and `qsort`. Do not use `chdir`, `nftw`, `fts`, `find`, or fixed path buffers. Submit `c1521_fs_017.c`.
