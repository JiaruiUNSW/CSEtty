# Q7 — Swap two integers through pointers

## Background

The caller owns two integer variables and passes their addresses to a helper. The helper must exchange the stored values rather than changing only local pointer variables.

## Requirements

Complete `swap` in `prac_q7.c`. After `swap(&a, &b)`, `a` must contain the original value of `b` and `b` the original value of `a`. Both pointers are valid and non-`NULL`. Do not change `main` or introduce global variables.

## Examples

```text
input: 3 9       output: 9 3
input: -4 12     output: 12 -4
input: 7 7       output: 7 7
```

## Implementation notes

Use a temporary integer and dereference both pointer parameters. Swapping the pointer variables themselves would not affect the caller. Submit `prac_q7.c`.

