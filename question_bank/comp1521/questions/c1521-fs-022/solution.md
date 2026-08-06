# Solution

## Approach

Parse hex pairs, then make a validation pass: each iteration requires two header bytes and at least `length` following bytes. If all records fit exactly, make a second pass to calculate each modular checksum and print.

## Correctness

The first pass advances by exactly `2 + length` for every complete record and rejects precisely when required bytes are unavailable, retaining the header offset. Once it reaches the end, the same partition is safe to traverse and each checksum includes every payload byte exactly once.

## Complexity

For `n` bytes, both passes take `O(n)` time and parsed storage is `O(n)`.

## Common pitfalls

Do not print partial results before discovering later truncation, mistake payload bytes for another header, or let unsigned arithmetic bypass the remaining-length check.
