# Solution

## Approach

Implement a recursive function that opens one directory, joins each entry path, and calls `lstat`. Recurse only for real directories. For regular files, compare the end of the basename with the suffix and update 64-bit totals.

## Correctness

Each reachable non-symlink directory is opened once and each child examined once. Recursive calls cover all descendant directories; regular matching children contribute exactly once, while all other types contribute zero. Therefore totals equal the specified set.

## Complexity

For `n` entries and maximum depth `h`, time is `O(n)` plus path construction and recursion stack is `O(h)`; transient path storage follows path length.

## Common pitfalls

Use `lstat`, not `stat`, compare suffix only when it is no longer than the name, skip both special entries, and propagate errors from deep recursion.
