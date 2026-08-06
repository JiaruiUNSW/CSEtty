# Threshold Exceedance Count — solution guide

## Approach

Read the count and threshold, then loop over the sequence and add one whenever the threshold is less than the current value.

## Correctness

For each input, the signed predicate is one exactly when that input exceeds the threshold. Its accumulated sum is therefore the count requested.

## Complexity

O(n) time and O(1) extra storage.

## Common pitfalls

Reversing `slt` counts values below the threshold. Using `<=` incorrectly counts equal values.
