# Solution

## Approach

Call `stat` once into a `struct stat`. Test `st_mode` with `S_ISREG` and `S_ISDIR`; print `st_size` only in the regular-file branch.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `regular-small`, runs `./c1521_fs_003 item`.
The test installs `tests/abc.txt -> item` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
regular 4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

On success, `stat` fills the metadata for the named object. The standard type macros partition the relevant cases, so the program prints exactly the specified label, and for a regular file `st_size` is its byte length.

## Complexity

The program performs one metadata lookup: `O(1)` user-space time and `O(1)` space, aside from filesystem lookup costs.

## Common pitfalls

Do not use bitwise tests such as `mode & S_IFREG`, print directory sizes, truncate `off_t` to `int`, or ignore a failed `stat` call.
