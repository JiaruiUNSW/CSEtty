# Row Champion — solution

## Approach

Compute sum and range for row zero, then scan later rows. Replace the champion on a larger sum or on an equal sum with a smaller range; leave exact ties unchanged.

## Correctness

After processing each prefix of rows, the stored champion is best under the lexicographic rules because it is updated exactly when the new row outranks it. Induction yields the global champion.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Do not initialise the best sum to zero, apply range only after a sum tie, and retain the earlier index for a complete tie. Verify boundary inputs as well as the worked example.

