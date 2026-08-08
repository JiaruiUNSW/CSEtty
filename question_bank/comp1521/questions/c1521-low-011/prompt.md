# Range Width Function

## Background

Read three signed integers. Call a function `range_width` with them in `$a0`–`$a2`; the function returns `max - min` in `$v0`. Print that result.

## Requirements

`main` must use `jal range_width`. The function must return with `jr $ra` and follow caller/callee register conventions.

Input constraints: all inputs are between -1000000 and 1000000.

Write your complete answer in `c1521_low_011.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
-2
8
3
```

the exact output is:

```text
10
```

## Implementation notes

A leaf function needs no stack frame if it only uses caller-saved temporaries. Find the minimum and maximum independently before subtracting.
