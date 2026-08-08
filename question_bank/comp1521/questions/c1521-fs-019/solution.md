# Solution

## Approach

Pass the current directory depth to a recursive walker, beginning at zero. A regular child increments count and bytes and compares that current depth with the maximum; a real directory child recurses with depth plus one.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `root-and-child`, runs `./c1521_fs_019 tree`.
The test installs `tests/aa.txt -> tree/a, tests/bbb.txt -> tree/sub/b` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
files=2 bytes=7 max_depth=1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The recursive call depth equals the number of directory edges below root. Every regular child is therefore recorded with exactly its containing-directory depth and is visited once. Sums accumulate every file, and repeated maximum updates yield the largest depth, or the initialized zero for none.

## Complexity

For `n` entries and depth `h`, time is `O(n)` and recursion/path space is `O(h)` plus current paths.

## Common pitfalls

Do not define root files as depth one, let empty directories affect maximum file depth, follow links, or discard a failure from a recursive call.
