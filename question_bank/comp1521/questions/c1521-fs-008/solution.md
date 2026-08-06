# Solution

## Approach

Parse into a wide unsigned integer, reject non-scalars, choose the canonical length from numeric boundaries, and extract successive six-bit groups. Add `0x80` to continuation groups and the appropriate lead prefix.

## Correctness

Each mask extracts exactly one disjoint six-bit portion of the scalar. Shifting places groups from most to least significant, while the prefixes encode the selected length. The boundary selection guarantees the shortest representation and validation excludes all non-scalars.

## Complexity

The program performs a bounded number of operations, so time and space are `O(1)`.

## Common pitfalls

Do not accept surrogates or U+110000, emit four bytes for a smaller value, forget two-digit zero padding, or parse a negative argument with an unsigned function without checking its sign.
