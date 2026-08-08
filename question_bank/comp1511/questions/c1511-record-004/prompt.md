# Equal-Reading Record Pairs

## Background

Named records combine a short identifier with one signed measurement. The identifier establishes input shape while the metric uses record order and values.

## Requirements

Read `n` (0 to 50), followed by `n` lines containing a whitespace-free name and signed value. Print `result: X`.

**Exact rule.** Count record-index pairs `i < j` with equal values; names do not affect equality.

Submit `c1511_record_004.c`. Your program must not print prompts or explanatory text.

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
result: 1
```

## Implementation notes

Represent each item with a `struct`; use a width limit when scanning the 31-character name.
