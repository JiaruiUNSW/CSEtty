# Recursive Triangular Function

## Background

Read `n`, call a recursive function `triangular(n)`, and print its return value. The base case `triangular(0)` is zero; otherwise it is `n + triangular(n-1)`.

## Requirements

Each non-base call must preserve `$ra` and its original argument on the stack. The stack pointer must have its incoming value when the function returns.

Input constraints: 0 <= n <= 1000 and the result fits signed 32 bits.

Write your complete answer in `c1521_low_024.s`. The program must not print prompts,
labels, debugging output, or extra whitespace. It must terminate with exit status
zero for every valid input.

## Examples

For this input:

```text
6
```

the exact output is:

```text
21
```

## Implementation notes

Allocate the frame before `jal`, save `$a0` and `$ra`, then restore both after the recursive call before adding the current term.
