# Q2 — Translate integer subtraction to MIPS

## Background

The starter program already reads two signed integers using the mipsy integer
input syscall. Your task is to finish the data movement and arithmetic that a
small C expression would require.

Conceptually, the program computes:

```c
result = first - second;
```

## Program requirements

Complete `final_q2.s` so that it:

1. reads the first signed integer;
2. reads the second signed integer;
3. subtracts the second value from the first;
4. prints the signed result followed by one newline; and
5. exits normally.

Keep the supplied syscall-based input and output. Do not print prompts or any
extra text. You may use temporary registers and arithmetic instructions
supported by mipsy.

## Examples

```text
$ printf '9\n4\n' | mipsy final_q2.s
5
$ printf '%s\n' -2 5 | mipsy final_q2.s
-7
```

## Implementation notes

After the second read, `$v0` contains the second number while the starter has
already preserved the first in `$t0`. The integer-print syscall expects the
answer in `$a0`.

