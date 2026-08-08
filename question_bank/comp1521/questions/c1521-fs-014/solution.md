# Solution

## Approach

Open the directory, skip only dot and dot-dot, join each name to the root, and call `lstat`. Store copied names and sizes for regular files in a growing array, then `qsort` by `strcmp` and print.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `sorted-files`, runs `./c1521_fs_014 scan`.
The test installs `tests/aa.txt -> scan/a.txt, tests/z.txt -> scan/z.bin` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
a.txt 3
z.bin 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every immediate entry is examined once. `lstat` identifies exactly regular non-symlink objects, so precisely the required entries enter the array. Sorting establishes the required total order, and printing each stored record yields the complete inventory.

## Complexity

For `n` entries and `r` regular files, scanning is `O(n)`, sorting `O(r log r)`, and stored space `O(r)` plus names.

## Common pitfalls

Never rely on `d_type` or `readdir` order, accidentally skip all dotfiles, follow symlinks with `stat`, or concatenate paths into a fixed buffer.
