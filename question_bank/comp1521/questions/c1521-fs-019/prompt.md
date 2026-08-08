# Measure recursive tree depth

## Background

Tree summaries can be computed during one recursive traversal. This task defines file depth by its containing directory so root-level files have depth zero.

## Requirements

- Write `c1521_fs_019.c`.
- Recursively walk the root directory without following symlinks.
- Count regular files, sum their byte sizes, and find the maximum file depth: a file directly under root is depth 0, under one subdirectory depth 1, and so on.
- Print `files=N bytes=B max_depth=D`; if there are no regular files, `D` is 0.
- Any traversal failure prints `c1521_fs_019: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_019 tree
```

Files provided for this example:

- `tree/a` (3 bytes) contains:

  ```text
  aa
  ```
- `tree/sub/b` (4 bytes) contains:

  ```text
  bbb
  ```

Output:

```text
files=2 bytes=7 max_depth=1
```

## Implementation notes

Use `opendir`, `readdir`, and `lstat`; skip special entries and ignore non-file, non-directory objects. Do not use shell commands, `nftw`, or symlink traversal. Submit `c1521_fs_019.c`.
