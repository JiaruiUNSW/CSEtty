# Solution

## Approach

Parse the requested byte with `strtol`, open the file read-only, and repeatedly read a buffer. Compare each returned byte with the target and increment a 64-bit counter. Retry an interrupted read and close the descriptor before printing.

## Correctness

Every successful `read` returns the next non-overlapping chunk of the file. The inner loop examines every byte in that chunk exactly once, adding one exactly when it equals the target. At end of file, the counter therefore equals the number of matching bytes in the complete file.

## Complexity

For a file of `n` bytes, time is `O(n)` and auxiliary space is `O(1)` because the buffer size is fixed.

## Common pitfalls

Do not call string functions on arbitrary bytes, assume a read fills the buffer, store `read`'s signed result in an unsigned type, or forget to treat `EINTR` separately.
