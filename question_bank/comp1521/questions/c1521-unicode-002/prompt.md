# UTF-8 Encoded Width

## Task

Return the canonical UTF-8 width: 1 for `0..0x7F`, 2 for `0x80..0x7FF`, 3 for `0x800..0xFFFF`, and 4 above that; return -1 for a non-scalar.

## Background

A Unicode boundary utility receives one numeric code point and must reason about scalar validity and variable-width encodings without depending on locale.

## Requirements

Read one hexadecimal code point and print the computed value as `result: X` followed by one newline. Surrogates and values above U+10FFFF are invalid and use the task rule's stated invalid result.

## Starter code

Complete `static long long solve(uint32_t cp)`. The supplied `main` reads the hexadecimal code point and prints the returned value.

## Examples

Input:

```text
000020ac
```

Output:

```text
result: 3
```

## Implementation notes

Derive UTF-8 fields with masks and shifts. Validate scalar range before encoding.

## Submission

Submit `c1521_unicode_002.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
