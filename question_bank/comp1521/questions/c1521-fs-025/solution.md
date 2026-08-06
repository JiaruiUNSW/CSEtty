# Solution

## Approach

On entering a directory, append a report record initialized to zero. Scan its children: add regular-file sizes to that record and recurse on real directories with a constructed relative path. After traversal, sort all directory records and print.

## Correctness

Every reachable directory creates exactly one record. Each regular file is encountered exactly in its containing directory and adds only to that directory's record, so direct byte totals are exact. Sorting all records yields the required global order, including zero-total directories.

## Complexity

For `n` entries and `d` directories, traversal is `O(n)`, sorting `O(d log d)`, and stored records/paths use `O(d)` space plus recursion depth.

## Common pitfalls

Do not compute recursive subtree totals, omit empty intermediate directories, confuse root's physical path with `.`, or retain a pointer into an array across `realloc`.
