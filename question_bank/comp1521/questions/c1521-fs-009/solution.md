# Solution

## Approach

Convert each pair of hex digits into one byte. At each offset, validate the entire next UTF-8 sequence using lead-byte and special second-byte ranges. Advance by its length and count it, or immediately print the current offset.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `valid-ascii`, runs `./c1521_fs_009 6162`.

Input:

```text
(empty)
```

Expected standard output:

```text
valid 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Hex conversion preserves the represented byte sequence. The validator accepts exactly canonical scalar encodings. Because validation begins at the first unconsumed offset and stops on the first failure, the reported offset is precisely the first sequence that cannot be decoded.

## Complexity

For `n` represented bytes, conversion and validation take `O(n)` time and `O(n)` storage.

## Common pitfalls

Report the lead offset rather than the continuation offset, reject overlong forms and surrogates, and do not treat malformed hex as malformed UTF-8 data.
