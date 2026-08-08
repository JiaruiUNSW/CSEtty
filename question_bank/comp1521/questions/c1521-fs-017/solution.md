# Solution

## Approach

Pass both a filesystem path and its relative counterpart through recursion. For each regular file, append a copied relative path and size to a dynamic array. After the full successful walk, sort all records by relative path and print.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `nested-order`, runs `./c1521_fs_017 tree`.
The test installs `tests/aa.txt -> tree/a.txt, tests/bbb.txt -> tree/sub/b.txt, tests/z.txt -> tree/z.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
a.txt 3
sub/b.txt 4
z.txt 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Recursive descent reaches every real descendant directory once, and `lstat` adds every regular file exactly once with the path components used to reach it. Global sorting produces the required order, so each printed line and the complete sequence are correct.

## Complexity

For `r` regular files among `n` entries, traversal is `O(n)`, sorting `O(r log r)`, and storage is `O(r)` plus path strings and recursion depth.

## Common pitfalls

Sorting each directory separately is not a substitute for an explicitly global ordering contract, and `stat` can follow links outside the root. Preserve relative and physical paths separately.
