# Worked solution — Q10

## Approach

Create the pipe before `fork`. The child closes the read end, computes the sum,
and calls a looped `write_all` helper before closing and exiting. The parent
closes the write end, fills one `long` with a looped `read_all`, closes the read
end, and accepts the value only after a successful `waitpid` result.

## Correctness

The child's loop adds each integer in `1..n` exactly once, so its local value is
the required sum. `write_all` advances only by bytes successfully written and
finishes only after all bytes of that value enter the pipe. Similarly,
`read_all` finishes only after the parent has reconstructed all bytes of one
`long`; EOF before that is an error. Since the parent also proves that the child
exited normally with status zero, the value it prints is exactly the complete
sum produced by the successful child.

## Complexity

The child performs O(n) additions. Transfer size and extra memory are O(1).

## Common pitfalls

- Leaving unused pipe ends open, which can prevent EOF.
- Assuming one `read` or `write` always transfers `sizeof(long)` bytes.
- Retrying every error instead of only `EINTR`.
- Printing before checking the child's encoded wait status.
- Returning from the child through parent code rather than using `_exit`.

