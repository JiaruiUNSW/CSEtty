# Solution

## Approach

Convert each pair of hex digits into one byte. At each offset, validate the entire next UTF-8 sequence using lead-byte and special second-byte ranges. Advance by its length and count it, or immediately print the current offset.

## Correctness

Hex conversion preserves the represented byte sequence. The validator accepts exactly canonical scalar encodings. Because validation begins at the first unconsumed offset and stops on the first failure, the reported offset is precisely the first sequence that cannot be decoded.

## Complexity

For `n` represented bytes, conversion and validation take `O(n)` time and `O(n)` storage.

## Common pitfalls

Report the lead offset rather than the continuation offset, reject overlong forms and surrogates, and do not treat malformed hex as malformed UTF-8 data.
