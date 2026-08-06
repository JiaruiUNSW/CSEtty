# Solution

## Approach

Parse hex into bytes, scan strict UTF-8, and store each sequence's starting offset and width. If validation succeeds, walk that table backwards and print the original bytes of each sequence.

## Correctness

Validation partitions the byte array into complete canonical scalar encodings. Traversing partitions in reverse changes only scalar order, while copying bytes within each partition in forward order preserves each scalar's encoding. Therefore the result is the required reversal.

## Complexity

For `n` bytes, time and storage are both `O(n)`.

## Common pitfalls

Do not reverse bytes inside a sequence, emit partial output before validation finishes, or forget that an empty hex string is valid empty UTF-8.
