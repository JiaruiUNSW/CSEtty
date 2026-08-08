# Swap binary records in place

## Background

In-place binary updates require positioned reads and complete writes. Record bytes are arbitrary; they cannot be passed to string functions.

## Requirements

- Write `c1521_fs_021.c`.
- Treat the regular file argument as consecutive four-byte records.
- Arguments two and three are valid non-negative record indices.
- Swap those records in place, then print the complete resulting file as continuous lowercase hexadecimal followed by newline.
- The same index is allowed and leaves data unchanged.
- Invalid size, index, arithmetic, or I/O prints `c1521_fs_021: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_021 records 0 1
```

Files provided for this example:

- `records` (16 bytes) contains:

  ```text
  AAAABBBBCCCCDDD
  ```

Output:

```text
4242424241414141434343434444440a
```

## Implementation notes

Use `open` with read/write access, `fstat`, `pread`, and a loop around `pwrite`. Do not load the file solely to perform the swap; a later streaming read for hexadecimal reporting is allowed. Submit `c1521_fs_021.c`.
