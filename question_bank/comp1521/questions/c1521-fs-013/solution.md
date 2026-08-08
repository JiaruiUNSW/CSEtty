# Solution

## Approach

Parse the hex string, then call a strict sequence-width function at each byte index. For nonzero width, print that many source bytes and advance by the width. For zero, print `efbfbd` and advance by one.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `already-valid`, runs `./c1521_fs_013 41c3a9`.

Input:

```text
(empty)
```

Expected standard output:

```text
41c3a9
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At each position there are exactly two cases. A valid sequence is copied as required and skipped as one unit. Otherwise the policy requires replacement of only that current byte, which the algorithm does before reconsidering the next byte. Induction over the advancing index proves the complete repaired output is exact.

## Complexity

For `n` bytes, time is `O(n)` and parsed storage is `O(n)`; each position inspects at most four bytes.

## Common pitfalls

Do not consume an entire malformed candidate, apply a library's different replacement policy, replace valid non-ASCII bytes, or emit binary output instead of requested hex.
