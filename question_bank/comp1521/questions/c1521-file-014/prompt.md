# Complete Four-Byte Records

## Background

A binary-safe command-line utility must derive one metric from a regular file without assuming text encoding or a terminating byte.

## Requirements

Accept exactly one file path, read the complete byte stream using POSIX file I/O, and print `result: X`. Empty files are valid.

**Exact rule.** Return the number of complete non-overlapping four-byte records, which is `file_size / 4` using integer division.

Submit `c1521_file_014.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `input.bin`
Fixture files: input.bin

Input:

```text
(empty)
```

Output:

```text
result: 1
```

## Implementation notes

Handle short reads and `read` errors, grow storage without losing the old pointer, and close the descriptor on every path.
