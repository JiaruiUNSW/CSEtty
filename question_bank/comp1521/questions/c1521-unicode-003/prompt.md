# UTF-8 Continuation Byte Count

## Background

A Unicode boundary utility receives one numeric code point and must reason about scalar validity and variable-width encodings without depending on locale.

## Requirements

Read one hexadecimal code point and print `result: X` for the operation in the title. Surrogates and values above U+10FFFF are invalid and use the stated invalid result.

**Exact rule.** Return the canonical UTF-8 width minus one, or -1 for a non-scalar.

Submit `c1521_unicode_003.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
000020ac
```

Output:

```text
result: 2
```

## Implementation notes

Derive UTF-8 fields with masks and shifts. Validate scalar range before encoding.
