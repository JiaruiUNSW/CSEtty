# Stable Sentinel Removal — solution

## Approach

Scan with a read index. Whenever an item differs from the sentinel, assign it at the write index and advance that index; then print the prefix of retained items.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `mixed`, runs `./c1511_core_011`.

Input:

```text
6 -1
3 -1 4 -1 5 6
```

Expected standard output:

```text
3 4 5 6
kept: 4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After each scan step, the prefix before the write index contains exactly the non-sentinel items seen so far in original order. The invariant proves the final prefix and returned length are correct.

## Complexity

O(n) time, O(n) input storage, and O(1) additional space.

## Common pitfalls

Advance the write index only for retained values. Format the empty result and spaces exactly. Also check every `scanf` target and preserve the required output format.
