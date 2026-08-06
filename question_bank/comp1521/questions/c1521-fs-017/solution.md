# Solution

## Approach

Pass both a filesystem path and its relative counterpart through recursion. For each regular file, append a copied relative path and size to a dynamic array. After the full successful walk, sort all records by relative path and print.

## Correctness

Recursive descent reaches every real descendant directory once, and `lstat` adds every regular file exactly once with the path components used to reach it. Global sorting produces the required order, so each printed line and the complete sequence are correct.

## Complexity

For `r` regular files among `n` entries, traversal is `O(n)`, sorting `O(r log r)`, and storage is `O(r)` plus path strings and recursion depth.

## Common pitfalls

Sorting each directory separately is not a substitute for an explicitly global ordering contract, and `stat` can follow links outside the root. Preserve relative and physical paths separately.
