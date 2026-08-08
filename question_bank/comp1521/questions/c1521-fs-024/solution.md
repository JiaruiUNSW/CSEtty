# Solution

## Approach

Parse the threshold, scan entries, and `lstat` joined child paths. Append the copied name and size when the object is regular and large enough, then sort by name and print.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `threshold`, runs `./c1521_fs_024 scan 3`.
The test installs `tests/two.txt -> scan/a, tests/four.txt -> scan/b, tests/one.txt -> scan/c` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
a 3
b 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every immediate child is tested once against both required predicates. Thus the stored array contains exactly qualifying regular files. `qsort` establishes the specified name order, so the output set and sequence are correct.

## Complexity

For `n` entries and `r` matches, traversal is `O(n)`, sorting `O(r log r)`, and storage `O(r)` plus names.

## Common pitfalls

Threshold equality must pass, directories must not, dotfiles are eligible, and a failed metadata lookup cannot simply be skipped. If fewer than two files match, skip `qsort`; this also avoids passing a null array pointer for the zero-result case.
