# Positive Wildlife Records

## Background

Named records combine a short identifier with one signed measurement. The identifier establishes input shape while the metric uses record order and values.

## Requirements

Read `n` (0 to 50), followed by `n` lines containing a whitespace-free name and signed value. Print `result: X`.

**Exact rule.** Count records whose value is strictly greater than zero.

Submit `c1511_record_002.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
4
a 3
b -1
c 3
d 8
```

Output:

```text
result: 3
```

## Implementation notes

Represent each item with a `struct`; use a width limit when scanning the 31-character name.
