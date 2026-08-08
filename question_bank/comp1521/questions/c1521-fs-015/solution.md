# Solution

## Approach

Implement a recursive function that opens one directory, joins each entry path, and calls `lstat`. Recurse only for real directories. For regular files, compare the end of the basename with the suffix and update 64-bit totals.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `nested-text`, runs `./c1521_fs_015 tree .txt`.
The test installs `tests/aa.txt -> tree/a.txt, tests/bbb.txt -> tree/sub/b.txt, tests/x.bin -> tree/sub/x.bin` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
files=2 bytes=7
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each reachable non-symlink directory is opened once and each child examined once. Recursive calls cover all descendant directories; regular matching children contribute exactly once, while all other types contribute zero. Therefore totals equal the specified set.

## Complexity

For `n` entries and maximum depth `h`, time is `O(n)` plus path construction and recursion stack is `O(h)`; transient path storage follows path length.

## Common pitfalls

Use `lstat`, not `stat`, compare suffix only when it is no longer than the name, skip both special entries, and propagate errors from deep recursion.
