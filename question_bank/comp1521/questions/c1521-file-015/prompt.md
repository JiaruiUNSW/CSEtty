# Position-Weighted Byte Checksum

## Background

A binary-safe command-line utility must derive one metric from a regular file without assuming text encoding or a terminating byte.

## Requirements

Accept exactly one file path, read the complete byte stream using POSIX file I/O, and print `result: X`. Empty files are valid.

**Exact rule.** Return `sum((i + 1) * byte[i]) modulo 2^31`, using unsigned bytes and one-based offsets.

Submit `c1521_file_015.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `input.bin`
Fixture files: input.bin

Input:

```text
(empty)
```

Output:

```text
result: 1368
```

## Implementation notes

Handle short reads and `read` errors, grow storage without losing the old pointer, and close the descriptor on every path.
