# Solution

## Approach

Parse the threshold, scan entries, and `lstat` joined child paths. Append the copied name and size when the object is regular and large enough, then sort by name and print.

## Correctness

Every immediate child is tested once against both required predicates. Thus the stored array contains exactly qualifying regular files. `qsort` establishes the specified name order, so the output set and sequence are correct.

## Complexity

For `n` entries and `r` matches, traversal is `O(n)`, sorting `O(r log r)`, and storage `O(r)` plus names.

## Common pitfalls

Threshold equality must pass, directories must not, dotfiles are eligible, and a failed metadata lookup cannot simply be skipped. If fewer than two files match, skip `qsort`; this also avoids passing a null array pointer for the zero-result case.
