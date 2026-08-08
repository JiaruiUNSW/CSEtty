# Solution

## Approach

Parse bytes and validate strict UTF-8 while recording no extra semantic data. After full validation, scan bytes again; subtract `0x20` only for values `0x61..0x7a`, then print every byte in hex.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `ascii-letters`, runs `./c1521_fs_011 61627a`.

Input:

```text
(empty)
```

Expected standard output:

```text
41425a
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Validation guarantees the input is well-formed. UTF-8 continuation and non-ASCII lead bytes are all at least 0x80, so none overlap the lowercase ASCII interval. The second pass therefore changes exactly the specified ASCII scalars and preserves every other encoding byte.

## Complexity

Parsing, validation, and transformation each take `O(n)` time; the byte array uses `O(n)` space.

## Common pitfalls

Do not transform before discovering a later error, apply locale case rules, change bytes inside multibyte sequences, or output uppercase hexadecimal digits.
