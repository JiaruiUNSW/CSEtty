# Solution

## Approach

Parse hex pairs, then make a validation pass: each iteration requires two header bytes and at least `length` following bytes. If all records fit exactly, make a second pass to calculate each modular checksum and print.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `one-record`, runs `./c1521_fs_022 0103414243`.

Input:

```text
(empty)
```

Expected standard output:

```text
1 3 198
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The first pass advances by exactly `2 + length` for every complete record and rejects precisely when required bytes are unavailable, retaining the header offset. Once it reaches the end, the same partition is safe to traverse and each checksum includes every payload byte exactly once.

## Complexity

For `n` bytes, both passes take `O(n)` time and parsed storage is `O(n)`.

## Common pitfalls

Do not print partial results before discovering later truncation, mistake payload bytes for another header, or let unsigned arithmetic bypass the remaining-length check.
