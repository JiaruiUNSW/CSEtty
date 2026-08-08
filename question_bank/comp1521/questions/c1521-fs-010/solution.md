# Solution

## Approach

Parse hex into bytes, scan strict UTF-8, and store each sequence's starting offset and width. If validation succeeds, walk that table backwards and print the original bytes of each sequence.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `ascii`, runs `./c1521_fs_010 616263`.

Input:

```text
(empty)
```

Expected standard output:

```text
636261
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Validation partitions the byte array into complete canonical scalar encodings. Traversing partitions in reverse changes only scalar order, while copying bytes within each partition in forward order preserves each scalar's encoding. Therefore the result is the required reversal.

## Complexity

For `n` bytes, time and storage are both `O(n)`.

## Common pitfalls

Do not reverse bytes inside a sequence, emit partial output before validation finishes, or forget that an empty hex string is valid empty UTF-8.
