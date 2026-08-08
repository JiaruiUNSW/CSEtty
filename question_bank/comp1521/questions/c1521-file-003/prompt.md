# Binary Zero Byte Count

## Task

Count bytes equal to hexadecimal `00`; embedded zero bytes are ordinary data.

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
result: 0
```

## Implementation notes

Treat the input as binary data: use `n`, not `strlen`, and compare each byte as an `unsigned char`. Do not change the supplied file-reading and cleanup code.

## Submission

Submit `c1521_file_003.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
