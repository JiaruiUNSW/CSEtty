# Decode Packed Sensor Records — solution guide

## Approach

For every word, mask its low byte into the score sum. Shift right eight, isolate a byte, sign-extend it, and add that signed value to the adjustment sum.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `two`, runs `mipsy c1521_low_025.s`.

Input:

```text
2
2688
61441
```

Expected standard output:

```text
129
-6
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The masks select exactly the declared fields. Arithmetic right shift replicates the extracted adjustment's sign bit, yielding its proper signed value, so both accumulators sum the specified record components.

## Complexity

O(n) time and O(1) storage.

## Common pitfalls

Using logical right shift for the final sign extension makes negative adjustments positive. Input records are decimal integers even though their layout is described in bits.
