# Select a Byte — solution guide

## Approach

Move the selected byte into bits 0..7 with a logical right shift and discard all higher bits with `& 0xff`.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `middle`, runs `./c1521_low_017`.

Input:

```text
1234abcd 1
```

Expected standard output:

```text
171
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Right-shifting by `8*i` maps exactly byte `i` to the low byte. The mask preserves those eight bits and clears every other bit, so the printed value is the requested byte.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Byte zero is the least-significant byte, independent of machine memory endianness. Avoid signed shifts and `%x`/type mismatches.
