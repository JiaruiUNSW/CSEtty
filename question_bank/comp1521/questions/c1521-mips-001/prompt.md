# MIPS Stream Total

## Background

A MIPS32 routine receives a pointer and element count after `main` reads a bounded integer stream. The routine must obey the register interface and return one scalar in `$v0`.

## Requirements

Read `n` (0 to 100) and `n` signed integers. `main` calls `solve($a0 = array, $a1 = n)`. Implement `solve`, return the title's metric in `$v0`, and let `main` print it with one newline.

**Exact rule.** Return the sum of all array elements, or 0 for an empty array.

Submit `c1521_mips_001.s`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
3
```

## Implementation notes

Use word-aligned loads, advance pointers by four bytes, and do not issue input/output syscalls inside `solve`.
