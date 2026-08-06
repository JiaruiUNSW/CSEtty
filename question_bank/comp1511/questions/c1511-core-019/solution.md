# Repair the Range Clamp — solution

## Approach

Compare the value with the lower bound first and return lower when needed; compare it with upper and return upper when needed; otherwise return the original value.

## Correctness

The three branches partition all integers into below, inside, and above the interval. Each branch returns exactly the value required for its partition.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Do not swap lower and upper returns, use strict comparisons so boundary values remain unchanged, and ensure every path returns. Keep the submitted filename and required output format unchanged.

