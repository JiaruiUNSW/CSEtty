# Count a byte with POSIX reads

## Background

Binary files are sequences of bytes; a byte does not become text merely because its value can represent a character. This task practises `open`, `read`, and `close` without relying on a terminating zero byte.

## Requirements

Write `c1521_fs_001.c`. Run it as `./c1521_fs_001 FILE BYTE`, where `BYTE` is a base-10 integer from 0 through 255. Read `FILE` with POSIX file I/O and print the number of bytes exactly equal to `BYTE`, followed by a newline. Process until `read` returns zero and correctly handle short reads. With invalid arguments, an invalid byte, or any system-call failure, print `c1521_fs_001: error\n` to standard error and return 1; otherwise return 0.

## Examples

If `fruit.dat` contains the seven bytes in `banana\n`, `./c1521_fs_001 fruit.dat 97` prints `3` because decimal 97 is the byte for lowercase `a`.

## Implementation notes

Use a fixed-size byte buffer; do not use `fopen`, `fgetc`, `mmap`, or external commands. The file may contain zero bytes and may be larger than memory. Submit only `c1521_fs_001.c`.
