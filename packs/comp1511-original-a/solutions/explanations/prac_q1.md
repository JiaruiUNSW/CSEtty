# Worked solution

## Approach

Traverse each node that has a successor. Count the pair when both values are non-zero and their explicit sign comparisons differ.

## Correctness

Every adjacent pair is visited exactly once. The condition accepts precisely positive/negative and negative/positive pairs, so zeros and equal-sign pairs are excluded.

## Complexity

Time is `O(n)` and extra space is `O(1)`.

## Common pitfalls

Multiplying values can overflow; stopping at `head` instead of `head->next` can dereference `NULL`; zero must break a sign transition.

