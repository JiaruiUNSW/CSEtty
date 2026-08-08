# Decode a compact TLV stream

## Background

Type-length-value formats place a one-byte type and one-byte payload length before each payload. Robust decoders must prove the entire record is available before consuming it.

## Requirements

- Write `c1521_fs_022.c`.
- Parse the hexadecimal argument into bytes.
- Each record is `TYPE LENGTH PAYLOAD...`, with unsigned one-byte fields.
- For every complete record print `TYPE LENGTH CHECKSUM`, where checksum is the payload-byte sum modulo 256.
- Empty input is valid and prints nothing.
- If a header or payload is truncated, print only `invalid O`, where `O` is that record's header offset; do not print earlier records.
- Bad hex syntax or arguments prints `c1521_fs_022: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_022 0103414243
```

Output:

```text
1 3 198
```

## Implementation notes

Validate the entire stream before producing output; a two-pass solution is acceptable. Accept either hex letter case. Do not read beyond the parsed array. Submit `c1521_fs_022.c`.
