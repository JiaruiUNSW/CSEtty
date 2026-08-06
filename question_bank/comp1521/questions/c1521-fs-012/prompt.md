# Profile UTF-8 sequence widths

## Background

A UTF-8 byte-length profile can estimate storage characteristics while still requiring full validation. Lead-byte counts alone are unsafe because malformed streams can mimic them.

## Requirements

Write `c1521_fs_012.c`. Decode the hexadecimal byte-string argument as strict UTF-8. On success print `one=A two=B three=C four=D`, counting canonical sequences of each width. On failure print `invalid O` for the failed sequence lead offset. Bad hex or arguments prints `c1521_fs_012: error\n` to standard error and returns 1.

## Examples

The encoding of one ASCII scalar, one two-byte scalar, one three-byte scalar, and one four-byte scalar prints one in every category.

## Implementation notes

Boundary checks must reject C0/C1 leads, overlong E0/F0 forms, surrogates under ED, and values above U+10FFFF under F4. Do not infer width without validating the required continuation bytes. Submit `c1521_fs_012.c`.
