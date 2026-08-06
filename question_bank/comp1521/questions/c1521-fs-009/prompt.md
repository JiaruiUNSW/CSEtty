# Locate malformed UTF-8

## Background

Diagnostics are more useful when they identify where decoding stopped. Hexadecimal input lets this exercise represent malformed byte streams without depending on terminal encoding.

## Requirements

Write `c1521_fs_009.c`. Its one argument is an even-length string of hexadecimal digits representing bytes. For strict UTF-8, print `valid N`, where `N` is the scalar count. Otherwise print `invalid O`, where `O` is the zero-based offset of the lead byte that cannot begin a complete valid sequence. For a bad continuation or truncation, report that sequence's lead offset. Odd length, non-hex syntax, or wrong arguments is a program error: print `c1521_fs_009: error\n` to standard error and return 1.

## Examples

`c3a9` prints `valid 1`; `61bf` prints `invalid 1`; overlong `c080` prints `invalid 0`.

## Implementation notes

Accept uppercase and lowercase hex. Enforce shortest encodings, exclude surrogates, and reject values above U+10FFFF. Do not decode through a locale API. Submit `c1521_fs_009.c`.
