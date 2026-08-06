# Worked solution

## Approach

Use an `if`, `else if`, `else` chain for less than zero, equal to zero, and greater than zero.

## Correctness

The three cases are disjoint and cover every integer, so exactly one required label is printed.

## Complexity

Time and extra space are `O(1)`.

## Common pitfalls

Using `<= 0` for the negative branch or printing extra prompts that break exact-output tests.

