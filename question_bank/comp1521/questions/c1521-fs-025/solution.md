# Solution

## Approach

On entering a directory, append a report record initialized to zero. Scan its children: add regular-file sizes to that record and recurse on real directories with a constructed relative path. After traversal, sort all directory records and print.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `root-and-child`, runs `./c1521_fs_025 tree`.
The test installs `tests/aa.txt -> tree/a, tests/bbb.txt -> tree/sub/b` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
. 3
sub 4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every reachable directory creates exactly one record. Each regular file is encountered exactly in its containing directory and adds only to that directory's record, so direct byte totals are exact. Sorting all records yields the required global order, including zero-total directories.

## Complexity

For `n` entries and `d` directories, traversal is `O(n)`, sorting `O(d log d)`, and stored records/paths use `O(d)` space plus recursion depth.

## Common pitfalls

Do not compute recursive subtree totals, omit empty intermediate directories, confuse root's physical path with `.`, or retain a pointer into an array across `realloc`.
