# Solution

## Approach

Validate file size is divisible by six, compare index with the quotient, and compute `index * 6`. Call `pread` for exactly six bytes, verify the final byte is newline, and write the first five.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `second-record`, runs `./c1521_fs_020 records 1`.
The test installs `tests/two_records.txt -> records` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
bravo
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Divisibility establishes a complete-record sequence. For an in-range index, fixed-width arithmetic identifies exactly its first byte and `pread` returns that record independently of descriptor position. The validated newline separates the data, so output is precisely the five-byte payload.

## Complexity

The operation reads a constant six bytes and uses `O(1)` time and space apart from filesystem lookup.

## Common pitfalls

Reject a partial final record, guard offset multiplication, handle a short `pread`, and do not treat payload bytes as a zero-terminated string.
