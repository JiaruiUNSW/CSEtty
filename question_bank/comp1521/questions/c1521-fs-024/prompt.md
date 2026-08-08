# Filter directory files by size

## Background

Metadata filters are common building blocks for cleanup and audit tools. Stable output requires explicit sorting and exact treatment of non-regular entries.

## Requirements

- Write `c1521_fs_024.c`.
- Arguments are a directory and a non-negative minimum byte size.
- Examine immediate entries with `lstat`; for every regular file whose size is at least the threshold, print `NAME SIZE` in bytewise name order.
- Ignore subdirectories, symbolic links, and other types.
- Invalid input or any directory, metadata, allocation, or close failure prints `c1521_fs_024: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_024 scan 3
```

Files provided for this example:

- `scan/a` (3 bytes) contains:

  ```text
  12
  ```
- `scan/b` (5 bytes) contains:

  ```text
  1234
  ```
- `scan/c` (2 bytes) contains:

  ```text
  1
  ```

Output:

```text
a 3
b 5
```

## Implementation notes

Do not recurse, use `d_type`, follow links, or invoke `find`. Include dotfiles except the two special directory entries and preserve large sizes. Submit `c1521_fs_024.c`.
