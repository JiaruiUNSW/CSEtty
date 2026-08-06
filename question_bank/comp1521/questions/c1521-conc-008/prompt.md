# Exec-Squared Workers

## Background

After `fork`, `exec` replaces the child image while preserving selected file descriptors. A program can deliberately exec itself in a private worker mode.

## Requirements

Write `c1521_conc_008.c`. Normal mode accepts one to six integers from -10000 to 10000. For each value create a dedicated pipe and child. In the child, redirect the pipe writer to standard output with `dup2`, close unrelated descriptors, and `execl` the same executable named by `argv[0]` with arguments `--worker VALUE`. Worker mode parses one value and prints only its signed square followed by newline. The parent reads and validates one integer line from every pipe, waits for each exact PID, and prints `INDEX square=VALUE` in input order. Failures return 1.

## Examples

Arguments `2 -3 10` produce squares 4, 9, and 100 in those positions even if workers finish in another order.

## Implementation notes

Only worker mode calculates and writes the square. Call `_exit(127)` if `execl` fails. The parent must not print pipe data until it has associated it with the correct index. Close all inherited pipe copies so EOF works, check wait status, and do not use `system` or a shell. Submit `c1521_conc_008.c`.
