# Copy a positioned byte range

## Background

Range extraction combines random access with robust streaming writes. The destination must be a fresh exact copy of only the available requested bytes.

## Requirements

- Write `c1521_fs_023.c`.
- Arguments are `SOURCE DESTINATION OFFSET LENGTH`, with non-negative decimal values.
- Create or truncate `DESTINATION`, then copy up to `LENGTH` bytes beginning at `OFFSET`; EOF may shorten the result.
- Print the number copied.
- Source and destination paths must differ as strings.
- Invalid values or any open/read/write/close error prints `c1521_fs_023: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_023 source out 2 4
```

Files provided for this example:

- `source` (11 bytes) contains:

  ```text
  abcdefghij
  ```

Output:

```text
4
```

## Implementation notes

Use `open`, `pread`, `write`, and `close`; handle short writes and interrupted calls. Use a fixed buffer, not a `LENGTH`-sized allocation. Do not invoke `dd`. Submit `c1521_fs_023.c`.
