# Warm Cross Centres — solution

## Approach

Visit every non-border cell, calculate the four-neighbour sum, compare it with four times the centre, and increment the result when strict inequality holds.

## Correctness

The nested loops visit every eligible interior cell exactly once. The integer inequality is algebraically equivalent to centre greater than neighbour average, so each visit is classified exactly.

## Complexity

O(rows * columns) time and O(rows * columns) space.

## Common pitfalls

Do not read neighbours for border cells. Equality is not warm, and diagonal cells are not neighbours. Also check every `scanf` target and preserve the required output format.

