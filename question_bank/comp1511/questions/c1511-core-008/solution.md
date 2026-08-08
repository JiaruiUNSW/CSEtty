# Frame Balance Checksum — solution

## Approach

Traverse every cell once. Add border cells to the accumulator and subtract non-border cells.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `square-two`, runs `./c1511_core_008`.

Input:

```text
2 2
1 2
3 4
```

Expected standard output:

```text
checksum: 10
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every cell is uniquely classified as border or interior. The traversal contributes each border value with coefficient +1 and each interior value with coefficient -1, exactly matching the checksum.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Independent loops over four edges can double-count corners. A single border predicate avoids that problem. Also check every `scanf` target and preserve the required output format.
