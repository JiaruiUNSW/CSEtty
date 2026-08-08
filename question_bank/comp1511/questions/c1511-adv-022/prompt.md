# Find the first signed decimal

## Background

`int first_decimal(const char *text, int *value)` finds the first decimal integer token and stores it through `value`, returning 1 on success and 0 otherwise.

## Requirements

- A token is digits optionally preceded immediately by `+` or `-`; a sign not followed by a digit is skipped.
- Search resumes after invalid characters, and stop after the first valid token.
- Assume a found integer fits in `int`; do not call `atoi`, `strtol`, or `sscanf`.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_022 'abc -42x'
```

Output:

```text
-42
```

## Implementation notes

Exactly one text argument is supplied. Cast to `unsigned char` before passing bytes to `isdigit`. Submit `c1511_adv_022.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
