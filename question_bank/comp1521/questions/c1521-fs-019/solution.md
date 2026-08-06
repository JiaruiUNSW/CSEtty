# Solution

## Approach

Pass the current directory depth to a recursive walker, beginning at zero. A regular child increments count and bytes and compares that current depth with the maximum; a real directory child recurses with depth plus one.

## Correctness

The recursive call depth equals the number of directory edges below root. Every regular child is therefore recorded with exactly its containing-directory depth and is visited once. Sums accumulate every file, and repeated maximum updates yield the largest depth, or the initialized zero for none.

## Complexity

For `n` entries and depth `h`, time is `O(n)` and recursion/path space is `O(h)` plus current paths.

## Common pitfalls

Do not define root files as depth one, let empty directories affect maximum file depth, follow links, or discard a failure from a recursive call.
