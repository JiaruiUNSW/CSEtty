# Weighted Letter Checksum — solution

## Approach

Stream characters, map each to a letter value, increment an accepted-letter position only for nonzero values, and add position times value.

## Correctness

Every accepted letter receives exactly its rank among accepted letters and its case-insensitive alphabet value. Non-letters add nothing and do not change ranks, matching the definition.

## Complexity

O(L) time and O(1) space.

## Common pitfalls

Do not advance the position for punctuation or digits, and map lowercase and uppercase to the same value. Keep the submitted filename and required output format unchanged.

