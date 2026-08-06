# Worked solution

## Approach

Iterate rows `1..rows-2` and columns `1..cols-2`, comparing each value with its four orthogonal neighbours.

## Correctness

The loop visits exactly the cells with four neighbours. A counter increment occurs exactly when all four required strict inequalities hold.

## Complexity

Time is `O(rows * cols)` and extra space is `O(1)`.

## Common pitfalls

Including borders, using diagonal neighbours, accepting equality, or swapping row and column bounds.

