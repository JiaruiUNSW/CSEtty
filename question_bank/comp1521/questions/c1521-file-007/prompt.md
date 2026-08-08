# Printable ASCII Byte Count

## Task

Count bytes in the inclusive printable-ASCII range `0x20` through `0x7E`.

## Background

A binary-safe command-line utility must inspect a regular file without assuming text encoding or a terminating zero byte.

## Requirements

The program accepts exactly one file path. The supplied code reads its complete byte stream and passes the bytes to `solve`. Print the computed value as `result: X` followed by one newline. Empty files are valid.

## Starter code

Complete `static long long solve(const unsigned char *data, size_t n)`. The supplied `main` already opens the named file, reads every byte, closes it, and frees the buffer.

## Examples

Command-line arguments: `input.bin`

Files provided for this example:

- `input.bin` contains:

  ```text
  A1b2C3
  ```

Output:

```text
result: 6
```

## Implementation notes

Treat the input as binary data: use `n`, not `strlen`, and compare each byte as an `unsigned char`. Do not change the supplied file-reading and cleanup code.

## Submission

Submit `c1521_file_007.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
