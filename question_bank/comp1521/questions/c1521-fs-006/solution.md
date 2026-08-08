# Solution

## Approach

Parse a strictly positive unsigned record size, call `stat`, verify `S_ISREG`, and divide `st_size` by that value. The quotient is the record count and the remainder is the trailing-byte count.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `exact-records`, runs `./c1521_fs_006 data 4`.
The test installs `tests/seven.txt -> data` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
records=2 trailing=0
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Euclidean division states that file size equals `R * RECORD_SIZE + T` with `0 <= T < RECORD_SIZE`. Integer quotient and remainder therefore produce exactly the required complete-record count and incomplete suffix length.

## Complexity

One metadata lookup and constant arithmetic require `O(1)` time and space in user code.

## Common pitfalls

Reject record size zero, directories, negative strings, and overflow. Do not cast file size to `int` or round up a partial record.
