# Stable Sentinel Removal — solution

## Approach

Scan with a read index. Whenever an item differs from the sentinel, assign it at the write index and advance that index; then print the prefix of retained items.

## Correctness

After each scan step, the prefix before the write index contains exactly the non-sentinel items seen so far in original order. The invariant proves the final prefix and returned length are correct.

## Complexity

O(n) time, O(n) input storage, and O(1) additional space.

## Common pitfalls

Advance the write index only for retained values. Format the empty result and spaces exactly. Also check every `scanf` target and preserve the required output format.

