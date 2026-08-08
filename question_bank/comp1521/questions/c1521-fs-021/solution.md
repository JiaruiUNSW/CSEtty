# Solution

## Approach

Validate the file length and indices, positioned-read both four-byte records, and positioned-write them to opposite offsets with a complete-write helper. Seek to the start only for the final buffered hex dump.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `first-two`, runs `./c1521_fs_021 records 0 1`.
The test installs `tests/four_records.txt -> records` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
4242424241414141434343434444440a
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The two reads capture original record values before any mutation. Writing the second value at the first offset and the first at the second changes exactly those records and preserves all others. Equal offsets write identical captured bytes, leaving the file unchanged.

## Complexity

The swap itself is `O(1)` time and memory. Reporting a file of `n` bytes costs `O(n)` time with `O(1)` buffered space.

## Common pitfalls

Do not overwrite one record before saving it, assume `pwrite` writes all bytes, accept a partial final record, or print signed bytes without zero padding.
