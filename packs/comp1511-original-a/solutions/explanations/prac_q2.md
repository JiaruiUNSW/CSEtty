# Worked solution

## Approach

Visit every cell and add it when its row or column is an extreme index.

## Correctness

The predicate is true for every border cell and false for every interior cell. Each coordinate is visited once, so corners are not duplicated.

## Complexity

Time is `O(size^2)` and extra space is `O(1)`.

## Common pitfalls

Adding four sides separately double-counts corners; size one needs to count its only cell once.

