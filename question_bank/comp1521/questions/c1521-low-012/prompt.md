# Sum of Squares by Function Call

## Background

Read `n`, followed by `n` integers. For each value, call `square`, a leaf function receiving `$a0` and returning its square in `$v0`. Print the sum of squares.

## Requirements

The loop must invoke `jal square` once per element. The final sum and every individual square fit in signed 32 bits.

Input constraints: 0 <= n <= 20 and -1000 <= each value <= 1000.

Write your complete answer in `c1521_low_012.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
3
2
-3
4
```

the exact output is:

```text
29
```

## Implementation notes

Values in caller-saved registers may be changed by a function. Keep the persistent loop state in `$s` registers or save it before each call.
