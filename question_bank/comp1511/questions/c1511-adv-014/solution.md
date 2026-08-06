# Solution: Compact neighbouring repeats

## Approach

If nonempty, retain the first value and scan each later value. Copy it to the next write position only when it differs from the last retained value.

## Correctness

After every read step, the written prefix contains exactly one representative for every complete run seen so far. A changed value starts a new run and is copied; an equal value belongs to the current run and is skipped.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Comparing against the previous unread element after overwriting, returning the original length, or reading element zero for empty input. Keep ownership clear: only free allocations owned by the caller or explicitly returned by the target function, and never dereference a zero-length array.
