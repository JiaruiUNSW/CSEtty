# Range Width Function — solution guide

## Approach

Pass the three inputs as arguments. In the leaf function, scan them to update local minimum and maximum registers, then return their difference.

## Correctness

After each argument is considered, the two candidate registers contain the minimum and maximum seen. Thus after all three, their difference is exactly the range width.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Do not jump back to a hard-coded label instead of using `$ra`. Signed comparisons are required, and the returned value must survive until `main` prints it.
