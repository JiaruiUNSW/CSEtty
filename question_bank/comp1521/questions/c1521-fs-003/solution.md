# Solution

## Approach

Call `stat` once into a `struct stat`. Test `st_mode` with `S_ISREG` and `S_ISDIR`; print `st_size` only in the regular-file branch.

## Correctness

On success, `stat` fills the metadata for the named object. The standard type macros partition the relevant cases, so the program prints exactly the specified label, and for a regular file `st_size` is its byte length.

## Complexity

The program performs one metadata lookup: `O(1)` user-space time and `O(1)` space, aside from filesystem lookup costs.

## Common pitfalls

Do not use bitwise tests such as `mode & S_IFREG`, print directory sizes, truncate `off_t` to `int`, or ignore a failed `stat` call.
