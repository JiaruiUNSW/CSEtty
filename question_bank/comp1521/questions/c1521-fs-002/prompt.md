# Round-trip big-endian words

## Background

A binary file format must choose a byte order rather than expose the host machine's representation. This program creates and verifies a simple stream of unsigned 32-bit big-endian words.

## Requirements

- Write `c1521_fs_002.c`.
- The single argument is an output filename.
- Read zero or more base-10 integers, one per line, from standard input; each must be in `0..4294967295`.
- Write each value as exactly four bytes, most significant byte first.
- Close and reopen the file, decode every complete word, and print `count=N checksum=S`, where `S` is the sum modulo 2^32.
- Invalid input or any I/O failure must print `c1521_fs_002: error\n` to standard error, return 1, and never print a success line.

## Examples

Command:

```text
./c1521_fs_002 words.bin
```

Input:

```text
1
256
65537
```

Output:

```text
count=3 checksum=65794
```

## Implementation notes

Use `fopen`, `fread`, and `fwrite`, but construct and decode the four bytes explicitly. Do not write a C `uint32_t` object directly, use byte-order helper libraries, or invoke another program. Submit `c1521_fs_002.c`.
