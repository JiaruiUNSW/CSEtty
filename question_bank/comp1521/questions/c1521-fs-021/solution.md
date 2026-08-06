# Solution

## Approach

Validate the file length and indices, positioned-read both four-byte records, and positioned-write them to opposite offsets with a complete-write helper. Seek to the start only for the final buffered hex dump.

## Correctness

The two reads capture original record values before any mutation. Writing the second value at the first offset and the first at the second changes exactly those records and preserves all others. Equal offsets write identical captured bytes, leaving the file unchanged.

## Complexity

The swap itself is `O(1)` time and memory. Reporting a file of `n` bytes costs `O(n)` time with `O(1)` buffered space.

## Common pitfalls

Do not overwrite one record before saving it, assume `pwrite` writes all bytes, accept a partial final record, or print signed bytes without zero padding.
