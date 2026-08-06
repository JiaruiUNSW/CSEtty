# Decode Packed Sensor Records — solution guide

## Approach

For every word, mask its low byte into the score sum. Shift right eight, isolate a byte, sign-extend it, and add that signed value to the adjustment sum.

## Correctness

The masks select exactly the declared fields. Arithmetic right shift replicates the extracted adjustment's sign bit, yielding its proper signed value, so both accumulators sum the specified record components.

## Complexity

O(n) time and O(1) storage.

## Common pitfalls

Using logical right shift for the final sign extension makes negative adjustments positive. Input records are decimal integers even though their layout is described in bits.
