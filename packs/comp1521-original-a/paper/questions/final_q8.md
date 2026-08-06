# Q8 — Find the maximum of five integers in MIPS

## Background

A robust maximum scan initialises its candidate from actual input. Initialising
the maximum to zero is incorrect when every input is negative.

## Program requirements

Complete `final_q8.s` so that it:

1. reads exactly five signed integers from standard input;
2. finds the greatest using signed comparisons;
3. prints that value followed by a newline; and
4. exits normally.

Use a loop for the remaining inputs after initialising the maximum from the
first value. Do not store all five values in memory and do not print prompts.

## Examples

```text
$ printf '3\n9\n-2\n7\n4\n' | mipsy final_q8.s
9
$ printf '%s\n' -8 -3 -11 -4 -6 | mipsy final_q8.s
-3
```

## Implementation notes

Keep the current maximum and remaining-input count in separate registers. A
branch can skip the update whenever the newly read value is less than or equal
to the current maximum.

