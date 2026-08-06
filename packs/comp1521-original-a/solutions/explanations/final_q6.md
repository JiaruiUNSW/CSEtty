# Worked solution — Q6

## Approach

Repeat 32 times: mask the low bit with `andi`, add that zero-or-one value to the
count, logically shift the input one position right, and decrement a separate
iteration counter.

## Correctness

On iteration i, the low bit of the shifted working value is original bit i.
Masking adds one exactly when that bit is set. After 32 iterations every
original bit position 0 through 31 has been counted once, and no other value is
added. The result is therefore the population count of the complete word,
including for negative two's-complement inputs.

## Complexity

The loop always performs 32 iterations, so time and extra space are O(1).

## Common pitfalls

- Stopping when the value reaches zero and mishandling negative input.
- Using arithmetic right shift, which replicates the sign bit.
- Testing fewer than all 32 bit positions.

