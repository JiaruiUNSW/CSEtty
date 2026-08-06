# Repair invalid UTF-8 bytes

## Background

Some byte-oriented importers need a deterministic recovery policy. This problem deliberately defines a simple policy rather than the more complex Unicode maximal-subpart recommendation.

## Requirements

Write `c1521_fs_013.c`. Parse one hexadecimal byte string. Scan left to right. If the bytes at the current position begin a complete strict UTF-8 scalar, copy that entire sequence unchanged. Otherwise replace exactly the single current byte with UTF-8 U+FFFD (`efbfbd`) and advance one byte. Print the repaired bytes as continuous lowercase hex. Bad hex syntax or arguments prints `c1521_fs_013: error\n` to standard error and returns 1.

## Examples

`41bf42` becomes `41efbfbd42`. Under this problem's one-byte policy, overlong pair `c0af` produces two replacement scalars, not one.

## Implementation notes

A failed attempted sequence does not consume its following bytes; they are reconsidered independently. Preserve every complete canonical sequence byte-for-byte. An empty input prints an empty line. Submit `c1521_fs_013.c`.
