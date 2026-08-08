# MIPS Positive Reading Count

## Task

Count elements strictly greater than zero; zero does not count.

## Background

A MIPS32 routine receives a pointer and element count after `main` reads a bounded integer stream. The routine must obey the register interface and return one scalar in `$v0`.

## Requirements

Read `n` (0 to 100) and `n` signed integers. `main` calls `solve($a0 = array, $a1 = n)`. Implement `solve`, return the computed value in `$v0`, and let `main` print it with one newline.

## Starter code

Complete the `solve` label only. It receives the array address in `$a0` and its length in `$a1`, and must return the result in `$v0`; the supplied `main` handles all syscalls.

## Examples

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
2
```

## Implementation notes

Use word-aligned loads, advance pointers by four bytes, and do not issue input/output syscalls inside `solve`.

## Submission

Submit `c1521_mips_002.s` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
