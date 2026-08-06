# Solution

## Approach

Convert hex pairs to bytes and reuse a strict sequence-width validator. For each valid sequence, increment the counter indexed by width and advance by that width.

## Correctness

The validator returns a width only for a complete canonical scalar encoding. Every successful iteration consumes exactly one such encoding, so incrementing the associated width bucket counts each scalar once in the correct category. First failure is reported at its current offset.

## Complexity

For `n` bytes, time is `O(n)` and the parsed byte array uses `O(n)` space.

## Common pitfalls

Do not count continuation bytes independently, accept truncated sequences, or report the byte after the invalid lead as the failure offset.
