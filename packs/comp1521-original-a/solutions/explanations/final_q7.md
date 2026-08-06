# Worked solution — Q7

## Approach

Call `fork`. The child calls `_exit(requested & 255)`. The parent waits for that
PID with `waitpid`, confirms `WIFEXITED(status)`, extracts
`WEXITSTATUS(status)`, and prints it.

## Correctness

There is exactly one child. Its only post-fork action is to terminate with the
requested eight-bit status. Waiting for the returned child PID ensures the
parent observes that process rather than an unrelated child. When
`WIFEXITED` is true, `WEXITSTATUS` is defined and equals the status supplied by
the child, so the printed number is the requested value.

## Complexity

The program performs O(1) work and uses O(1) memory, in addition to creating one
process.

## Common pitfalls

- Printing the raw encoded wait status.
- Calling `WEXITSTATUS` without first checking `WIFEXITED`.
- Letting the child fall through into the parent's wait/print path.
- Using buffered `exit` in a forked child when `_exit` is the safer primitive.

