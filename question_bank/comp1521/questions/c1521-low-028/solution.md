# Classify a Binary32 Encoding — solution guide

## Approach

Branch on exponent zero, exponent 255, or an intermediate exponent. Within each special exponent, distinguish a zero fraction from a nonzero fraction.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `infinity`, runs `./c1521_low_028`.

Input:

```text
7f800000
```

Expected standard output:

```text
infinity
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

IEEE-754 defines zero/subnormal for exponent zero, infinity/NaN for exponent all ones, and normal for every intermediate exponent. Fraction zero selects the first class in each special pair.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Do not cast or evaluate the bits as a host float; classification is a bit-field task. Negative zero is still `zero`.
