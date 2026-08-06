# Select a Byte — solution guide

## Approach

Move the selected byte into bits 0..7 with a logical right shift and discard all higher bits with `& 0xff`.

## Correctness

Right-shifting by `8*i` maps exactly byte `i` to the low byte. The mask preserves those eight bits and clears every other bit, so the printed value is the requested byte.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Byte zero is the least-significant byte, independent of machine memory endianness. Avoid signed shifts and `%x`/type mismatches.
