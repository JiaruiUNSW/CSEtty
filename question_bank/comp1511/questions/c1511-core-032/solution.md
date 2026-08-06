# Most Improved Student — solution

## Approach

Read all records, select the first as current best, and replace it when a later record has a larger gain or wins the stated tie breakers.

## Correctness

The comparison helper exactly implements the ordered ranking keys. Maintaining the best record over each scanned prefix therefore yields the unique required winner after the final record.

## Complexity

O(n) time and O(n) space.

## Common pitfalls

Subtract before from after, apply tie breakers in order, and do not use zero as an initial best gain. Verify boundary inputs as well as the worked example.

