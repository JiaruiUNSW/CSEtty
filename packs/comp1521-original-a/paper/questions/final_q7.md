# Q7 — Inspect a child process exit status

## Background

`fork` creates a child process, but the integer returned by `waitpid` through
its status pointer is encoded. A parent must first confirm that the child exited
normally and then extract the eight-bit exit status with the macros from
`<sys/wait.h>`.

## Program requirements

Complete `final_q7.c`. It receives one decimal integer from 0 through 255 and
must:

1. call `fork` exactly once;
2. make the child terminate immediately with that requested status;
3. make the parent wait for that specific child;
4. verify that the child exited normally; and
5. print the decoded exit status followed by a newline.

Use `_exit` in the child. Use `waitpid`, `WIFEXITED`, and `WEXITSTATUS` in the
parent. Return non-zero after a failed `fork` or `waitpid`. Do not launch an
external command and do not simply print the command-line number from the
parent.

## Examples

```text
$ ./final_q7 7
7
$ ./final_q7 0
0
```

## Implementation notes

After `fork`, only the child branch should call `_exit`; only the parent branch
should call `waitpid` and print. Keeping those paths visibly separate makes
accidental duplicate output less likely.

