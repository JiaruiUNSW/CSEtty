# Weighted Letter Checksum — solution

## Approach

Stream characters, map each to a letter value, increment an accepted-letter position only for nonzero values, and add position times value.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `mixed`, runs `./c1511_core_028`.

Input:

```text
A-bC!
```

Expected standard output:

```text
checksum: 14
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every accepted letter receives exactly its rank among accepted letters and its case-insensitive alphabet value. Non-letters add nothing and do not change ranks, matching the definition.

## Complexity

O(L) time and O(1) space.

## Common pitfalls

Do not advance the position for punctuation or digits, and map lowercase and uppercase to the same value. Keep the submitted filename and required output format unchanged.
