# Streaming Total — solution guide

## Approach

Initialise index and sum to zero. While index is less than `n`, read the next integer, add it to the sum, and increment the index.

## Correctness

The loop invariant states that the sum register contains exactly the first `index` values. When `index=n`, all and only the requested inputs have been accumulated.

## Complexity

O(n) time and O(1) extra storage.

## Common pitfalls

Do not include `n` itself in the sum. Check the loop condition before reading, otherwise the empty case consumes a nonexistent value.
