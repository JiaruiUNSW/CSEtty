# Sign-Extend a Twelve-Bit Field — solution guide

## Approach

Retain the low 12 bits. If the field's sign bit is one, fill the upper twenty bits with ones, then convert the resulting 32-bit representation for decimal output.

## Correctness

Positive 12-bit encodings have sign bit zero and retain their numeric value. Negative encodings gain exactly the leading ones required by two's-complement sign extension, preserving their represented signed value.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Checking bit 31 tests the wrong sign. Subtracting 4096 works mathematically but misses the intended representation exercise.
