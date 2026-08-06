# Busiest Two-by-Two Window — solution

## Approach

Enumerate top rows zero through rows minus two and left columns zero through columns minus two, compute each four-cell sum, and replace the best only on a strict increase.

## Correctness

The loops visit every valid window exactly once. Strict replacement selects the greatest sum while leaving the first row-major window on ties, which implements both tie breakers.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Do not start windows on the last row or column, and do not replace the best on equal sums. Verify boundary inputs as well as the worked example.

