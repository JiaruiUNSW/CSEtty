# Solution

## Approach

Parse the requested byte with `strtol`, open the file read-only, and repeatedly read a buffer. Compare each returned byte with the target and increment a 64-bit counter. Retry an interrupted read and close the descriptor before printing.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `repeated-byte`, runs `./c1521_fs_001 input.dat 97`.
The test installs `tests/banana.txt -> input.dat` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every successful `read` returns the next non-overlapping chunk of the file. The inner loop examines every byte in that chunk exactly once, adding one exactly when it equals the target. At end of file, the counter therefore equals the number of matching bytes in the complete file.

## Complexity

For a file of `n` bytes, time is `O(n)` and auxiliary space is `O(1)` because the buffer size is fixed.

## Common pitfalls

Do not call string functions on arbitrary bytes, assume a read fills the buffer, store `read`'s signed result in an unsigned type, or forget to treat `EINTR` separately.
