# Child Exit Histogram

## Background

A process exit code is not the raw integer returned by `waitpid`. The parent must first determine how the child ended and then decode a normal exit status.

## Requirements

- Implement `c1521_conc_007.c`.
- Accept one to eight decimal codes, each from 0 through 7.
- Fork one child for every code; each child immediately terminates with that code using `_exit`.
- The parent must retain every PID, use `waitpid` on each exact PID, reject any abnormal termination, count decoded `WEXITSTATUS` values, and print nonzero histogram entries in ascending status order as `status S count=N`.
- Finish with `children=N`.
- Invalid input or a system-call failure returns 1.

## Examples

Command:

```text
./c1521_conc_007 0 1 1 3
```

Output:

```text
status 0 count=1
status 1 count=2
status 3 count=1
children=4
```

## Implementation notes

Validate all codes before creating children. Do not use the raw wait status as an exit code, and do not let children call `exit` after a fork because inherited stdio buffers may flush. Every successful fork must eventually be reaped, including when a later fork fails. Submit `c1521_conc_007.c`.
