# Solution

## Approach

Parse bytes and validate strict UTF-8 while recording no extra semantic data. After full validation, scan bytes again; subtract `0x20` only for values `0x61..0x7a`, then print every byte in hex.

## Correctness

Validation guarantees the input is well-formed. UTF-8 continuation and non-ASCII lead bytes are all at least 0x80, so none overlap the lowercase ASCII interval. The second pass therefore changes exactly the specified ASCII scalars and preserves every other encoding byte.

## Complexity

Parsing, validation, and transformation each take `O(n)` time; the byte array uses `O(n)` space.

## Common pitfalls

Do not transform before discovering a later error, apply locale case rules, change bytes inside multibyte sequences, or output uppercase hexadecimal digits.
