# Q10 — Most frequent lowercase letter

## Background

The program receives an arbitrary text stream and must summarise lowercase ASCII letter frequency.

## Requirements

Complete `prac_q10.c`. Read until end of input, count only characters from `'a'` through `'z'`, then print the most frequent lowercase letter, a space, its count, and a newline. Ignore uppercase letters and all other bytes. Resolve a tie by choosing the alphabetically earliest letter. If no lowercase letter appears, print `a 0`.

## Examples

```text
input: banana       output: a 3
input: cabbca       output: a 2
input: 123!         output: a 0
```

## Implementation notes

The supplied frequency array is indexed from zero for `a`. When scanning it, update the best index only for a strictly greater count; this naturally preserves the earliest letter on a tie. Submit `prac_q10.c`.

