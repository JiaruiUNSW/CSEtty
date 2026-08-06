# Solution

## Approach

Parse the hex string, then call a strict sequence-width function at each byte index. For nonzero width, print that many source bytes and advance by the width. For zero, print `efbfbd` and advance by one.

## Correctness

At each position there are exactly two cases. A valid sequence is copied as required and skipped as one unit. Otherwise the policy requires replacement of only that current byte, which the algorithm does before reconsidering the next byte. Induction over the advancing index proves the complete repaired output is exact.

## Complexity

For `n` bytes, time is `O(n)` and parsed storage is `O(n)`; each position inspects at most four bytes.

## Common pitfalls

Do not consume an entire malformed candidate, apply a library's different replacement policy, replace valid non-ASCII bytes, or emit binary output instead of requested hex.
