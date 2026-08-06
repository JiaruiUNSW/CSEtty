# Q10 — Transfer a range sum through a process pipe

## Background

This question combines process creation, anonymous pipes, descriptor ownership,
short I/O, and wait-status handling. A pipe is a byte stream: even when sending
one `long`, robust code must not assume that a single `read` or `write` transfers
all requested bytes.

## Program requirements

Complete `final_q10.c`. It receives one positive decimal integer `n` whose sum
fits in `long`. The program must:

1. create one anonymous pipe;
2. call `fork` exactly once;
3. have the child compute the inclusive sum `1 + 2 + ... + n` using a loop;
4. have the child write the binary `long` result to the pipe, retrying after
   `EINTR` and completing short writes;
5. have the parent read exactly one binary `long`, likewise handling `EINTR`
   and short reads;
6. close every unused pipe end promptly in both processes;
7. have the parent wait for the child and require a normal zero exit; and
8. print the received decimal result followed by a newline.

Do not send a text representation through the pipe, use shared memory, call an
external program, or compute the sum again in the parent. Return non-zero when
`pipe`, `fork`, data transfer, or `waitpid` fails.

## Examples

```text
$ ./final_q10 10
55
$ ./final_q10 100
5050
```

## Implementation notes

Small `read_all` and `write_all` helpers make the transfer contract explicit.
The child must close the read end before calculating; the parent must close the
write end before reading. Closing the correct ends is what allows EOF and error
conditions to behave predictably.

