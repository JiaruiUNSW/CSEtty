# Concurrent File Fingerprints

## Background

A file fingerprint can be computed independently for many files. Separate child processes provide isolation, while a pipe returns a small record to the parent.

## Requirements

- Implement `c1521_conc_002.c`.
- Accept between one and four file names.
- Fork one child per file and give each child its own pipe.
- A child must use `open` and `read` to count bytes and calculate the checksum equal to the sum of all unsigned byte values modulo 65536.
- The parent must reap every child and print `INDEX bytes=N checksum=C` in command-line order, regardless of completion order.
- Invalid argument counts or any system-call/file failure return 1.

## Examples

Command:

```text
./c1521_conc_002 a.bin b.bin
```

Files provided for this example:

- `a.bin` (4 bytes) contains:

  ```text
  abc
  ```
- `b.bin` (5 bytes) contains:

  ```text
  A
  B
  ```

Output:

```text
0 bytes=4 checksum=304
1 bytes=5 checksum=161
```

## Implementation notes

Treat data as `unsigned char`, because binary bytes above 127 must not sign-extend. Close inherited descriptors in every process. Use a complete-read/complete-write loop for records and `waitpid` with stored PIDs. Submit `c1521_conc_002.c`; do not invoke shell commands or create temporary files.
