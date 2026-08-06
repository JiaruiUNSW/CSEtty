# Negative Reading Tally — solution guide

## Approach

Loop over all readings, evaluate a signed less-than-zero predicate for each, and add that predicate to the tally.

## Correctness

The predicate contributes one exactly for a negative input and zero otherwise. Summing it over the full sequence therefore gives precisely the number of negative readings.

## Complexity

O(n) time and O(1) extra storage.

## Common pitfalls

Using an unsigned comparison makes every value non-negative. Do not treat zero as negative or stop early when the tally reaches a particular number.
