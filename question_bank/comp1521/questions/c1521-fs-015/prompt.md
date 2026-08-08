# Recursive suffix summary

## Background

Recursive file tools combine directory walking, metadata checks, and name filtering. Symlinks must not turn a finite tree walk into an escape or cycle.

## Requirements

- Write `c1521_fs_015.c`.
- Arguments are a root directory and a non-empty suffix.
- Recursively visit real directories below the root without following symbolic links.
- For every regular file whose basename ends with the suffix, add its byte size and count it.
- Print `files=N bytes=B`.
- Ignore other object types.
- Any traversal, metadata, allocation, or close error prints `c1521_fs_015: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_015 tree .txt
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
- `tree/sub/x.bin` (2 bytes) contains:

  ```text
  x
  ```

Output:

```text
files=2 bytes=7
```

## Implementation notes

Use `opendir`, `readdir`, and `lstat`; skip `.` and `..`. No output depends on traversal order. Do not use `nftw`, `fts`, `chdir`, `find`, or symlink following. Submit `c1521_fs_015.c`.
