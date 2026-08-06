# Solution

## Approach

Read the lead byte, determine its required length, and read its continuation bytes. Apply special second-byte ranges for E0, ED, F0, and F4; ordinary continuation bytes must be 80..BF. Increment the count only after a complete valid sequence.

## Correctness

The accepted lead and continuation ranges are exactly the canonical UTF-8 encodings of Unicode scalar values. Special ranges exclude overlong forms, surrogates, and out-of-range values. Each accepted sequence represents one scalar and sequences consume the stream without overlap, so the final count is exact.

## Complexity

For `n` input bytes, time is `O(n)` and auxiliary space is `O(1)`.

## Common pitfalls

Checking only `10xxxxxx` continuation prefixes accepts overlong and surrogate encodings. Use unsigned bytes, detect EOF mid-sequence, and distinguish EOF from `ferror`.
