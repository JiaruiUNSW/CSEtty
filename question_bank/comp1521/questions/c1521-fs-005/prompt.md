# Read a byte window

## Background

Random-access programs often inspect a bounded region without loading the prefix. A hexadecimal dump is also safer than treating arbitrary bytes as a C string.

## Requirements

- Write `c1521_fs_005.c`.
- Arguments are `FILE OFFSET LENGTH`, with non-negative decimal values.
- Seek to byte `OFFSET`, read at most `LENGTH` bytes, and print the bytes actually available as two lowercase hexadecimal digits separated by one space, then newline.
- Reaching EOF early is successful.
- Invalid arguments, an unrepresentable offset, or any I/O failure prints `c1521_fs_005: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_005 data 2 4
```

Files provided for this example:

- `data` (11 bytes) contains:

  ```text
  0123456789
  ```

Output:

```text
32 33 34 35
```

## Implementation notes

Use `open`, `lseek`, `read`, and `close`; do not read and discard the prefix. Process in a fixed buffer so very large requested lengths do not require a large allocation. Submit `c1521_fs_005.c`.
