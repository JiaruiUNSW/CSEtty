# Solution

## Approach

Open the directory, skip only dot and dot-dot, join each name to the root, and call `lstat`. Store copied names and sizes for regular files in a growing array, then `qsort` by `strcmp` and print.

## Correctness

Every immediate entry is examined once. `lstat` identifies exactly regular non-symlink objects, so precisely the required entries enter the array. Sorting establishes the required total order, and printing each stored record yields the complete inventory.

## Complexity

For `n` entries and `r` regular files, scanning is `O(n)`, sorting `O(r log r)`, and stored space `O(r)` plus names.

## Common pitfalls

Never rely on `d_type` or `readdir` order, accidentally skip all dotfiles, follow symlinks with `stat`, or concatenate paths into a fixed buffer.
