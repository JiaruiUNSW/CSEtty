# Count strict UTF-8 code points

## Background

UTF-8 encodes one Unicode scalar value in one to four bytes. Counting bytes, continuation bytes, or leading bytes alone does not establish that the stream is valid.

## Requirements

- Write `c1521_fs_007.c`.
- Read all bytes from standard input.
- If they form strict UTF-8, print the number of encoded Unicode scalar values followed by newline.
- If not, print `invalid\n` and still return 0.
- Reject stray continuation bytes, truncated sequences, overlong encodings, UTF-16 surrogate values, and values above U+10FFFF.
- A standard-input read failure prints `c1521_fs_007: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_007
```

Input:

```text
abc
```

Output:

```text
3
```

## Implementation notes

Decode unsigned bytes explicitly. U+0000 is valid input data. Do not call locale-dependent multibyte functions, assume input is newline terminated, or store the whole stream. Submit `c1521_fs_007.c`.
