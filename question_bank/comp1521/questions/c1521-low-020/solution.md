# Sign-Extend a Twelve-Bit Field — solution guide

## Approach

Retain the low 12 bits. If the field's sign bit is one, fill the upper twenty bits with ones, then convert the resulting 32-bit representation for decimal output.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `negative`, runs `./c1521_low_020`.

Input:

```text
f80
```

Expected standard output:

```text
-128
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Positive 12-bit encodings have sign bit zero and retain their numeric value. Negative encodings gain exactly the leading ones required by two's-complement sign extension, preserving their represented signed value.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Checking bit 31 tests the wrong sign. Subtracting 4096 works mathematically but misses the intended representation exercise.
