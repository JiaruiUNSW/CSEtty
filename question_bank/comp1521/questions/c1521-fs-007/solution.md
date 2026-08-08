# Solution

## Approach

Read the lead byte, determine its required length, and read its continuation bytes. Apply special second-byte ranges for E0, ED, F0, and F4; ordinary continuation bytes must be 80..BF. Increment the count only after a complete valid sequence.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `ascii`, runs `./c1521_fs_007`.

Input:

```text
abc
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The accepted lead and continuation ranges are exactly the canonical UTF-8 encodings of Unicode scalar values. Special ranges exclude overlong forms, surrogates, and out-of-range values. Each accepted sequence represents one scalar and sequences consume the stream without overlap, so the final count is exact.

## Complexity

For `n` input bytes, time is `O(n)` and auxiliary space is `O(1)`.

## Common pitfalls

Checking only `10xxxxxx` continuation prefixes accepts overlong and surrogate encodings. Use unsigned bytes, detect EOF mid-sequence, and distinguish EOF from `ferror`.
