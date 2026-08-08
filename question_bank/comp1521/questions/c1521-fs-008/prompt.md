# Encode one Unicode scalar

## Background

UTF-8 partitions a scalar value into six-bit payload groups and adds length prefixes. Unicode scalar values explicitly exclude the UTF-16 surrogate interval.

## Requirements

- Write `c1521_fs_008.c`.
- Accept exactly one base-10 integer argument.
- For a Unicode scalar value U+0000..U+10FFFF excluding U+D800..U+DFFF, print its shortest UTF-8 encoding as lowercase two-digit bytes separated by spaces.
- For a numeric value outside that set, print `invalid\n` and return 0.
- Malformed numeric syntax or wrong arguments prints `c1521_fs_008: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_008 65
```

Output:

```text
41
```

## Implementation notes

Use shifts and masks. Select one byte through U+007F, two through U+07FF, three through U+FFFF, and four thereafter. Do not use locale conversion functions or Unicode libraries. Submit `c1521_fs_008.c`.
