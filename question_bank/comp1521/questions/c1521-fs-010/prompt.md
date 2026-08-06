# Reverse UTF-8 by scalar

## Background

Reversing raw bytes corrupts multibyte UTF-8. A scalar-aware reversal changes scalar order while preserving the byte sequence inside every encoding.

## Requirements

Write `c1521_fs_010.c`. Its argument is an even-length hexadecimal byte string. If it is strict UTF-8, output the same scalars in reverse order as one continuous lowercase hexadecimal string. An empty input produces an empty output line. For malformed UTF-8 print `invalid O`, using the lead-byte offset rule from the prompt. Malformed hex or wrong arguments prints `c1521_fs_010: error\n` to standard error and returns 1.

## Examples

Hex `41c3a9e78cab` encodes `Aé猫` and becomes `e78cabc3a941`. The truncated sequence `e282` prints `invalid 0`.

## Implementation notes

Validate canonical encodings before producing transformed output. You may store byte offsets proportional to input size. Do not decode into `wchar_t` or reverse individual bytes. Submit `c1521_fs_010.c`.
