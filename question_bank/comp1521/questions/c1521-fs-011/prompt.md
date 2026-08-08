# Uppercase ASCII inside UTF-8

## Background

ASCII bytes never occur as part of a multibyte UTF-8 encoding, so an ASCII-only case transformation can be byte-local after the complete stream has been validated.

## Requirements

- Write `c1521_fs_011.c`.
- Parse one hexadecimal byte-string argument.
- For strict UTF-8, replace every ASCII byte `a` through `z` with `A` through `Z` and print the result as continuous lowercase hex.
- Preserve all other bytes exactly.
- For malformed UTF-8 print `invalid O`, where `O` is the failed sequence's lead offset.
- Bad hex syntax or arguments prints `c1521_fs_011: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_011 61627a
```

Output:

```text
41425a
```

## Implementation notes

Validate the entire byte string before printing any transformed data. This is not full Unicode case folding: only ASCII lowercase changes. Do not call `toupper` on arbitrary bytes. Submit `c1521_fs_011.c`.
