# Solution

## Approach

Parse into a wide unsigned integer, reject non-scalars, choose the canonical length from numeric boundaries, and extract successive six-bit groups. Add `0x80` to continuation groups and the appropriate lead prefix.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `ascii`, runs `./c1521_fs_008 65`.

Input:

```text
(empty)
```

Expected standard output:

```text
41
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each mask extracts exactly one disjoint six-bit portion of the scalar. Shifting places groups from most to least significant, while the prefixes encode the selected length. The boundary selection guarantees the shortest representation and validation excludes all non-scalars.

## Complexity

The program performs a bounded number of operations, so time and space are `O(1)`.

## Common pitfalls

Do not accept surrogates or U+110000, emit four bytes for a smaller value, forget two-digit zero padding, or parse a negative argument with an unsigned function without checking its sign.
