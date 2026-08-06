# Q9 — Find the longest character run

## Background

A run is a maximal contiguous group of identical characters in a string. Only adjacency matters.

## Requirements

Complete `longest_run` in `prac_q9.c`. The argument is a valid, non-empty null-terminated string. Return the length of its longest run. The function must not modify the string, allocate memory, or perform I/O. The supplied `main` passes the single command-line argument and prints the result.

## Examples

```text
./prac_q9 abbcccdd
3

./prac_q9 z
1

./prac_q9 aabbaa
2
```

## Implementation notes

Maintain the current run and the best run seen so far. Start both at one because the string is non-empty, reset the current run when adjacent characters differ, and update the best after each character. Submit `prac_q9.c`.

