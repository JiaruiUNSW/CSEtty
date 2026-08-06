# Worked solution

## Approach

Scan from the second character, extending the current run when it matches its predecessor and resetting otherwise; retain the largest length.

## Correctness

At each position the current counter equals the run ending there, and the best counter is the maximum over every run seen so far.

## Complexity

Time is `O(n)` and extra space is `O(1)`.

## Common pitfalls

Starting at zero for a non-empty string, failing to reset to one, or counting total frequency instead of contiguous runs.

