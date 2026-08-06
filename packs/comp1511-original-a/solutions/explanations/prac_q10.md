# Worked solution

## Approach

Count lowercase letters in a 26-element array, then scan from `a` to `z`, replacing the best index only for a strictly larger count.

## Correctness

The first pass records exact frequencies. The second maintains the earliest index with maximum frequency, so the final pair satisfies both frequency and tie rules.

## Complexity

Time is `O(n + 26)` and extra space is `O(26)`.

## Common pitfalls

Using `>=` changes ties to the latest letter, counting uppercase input, or leaving the no-letter case undefined.

