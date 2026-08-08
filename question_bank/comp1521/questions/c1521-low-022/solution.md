# Saturating Signed Addition — solution guide

## Approach

Compute the wrapped unsigned sum. If both operands were non-negative and the result sign is one, return the maximum. If both were negative and the result sign is zero, return the minimum. Otherwise reinterpret the wrapped sum.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `positive_overflow`, runs `./c1521_low_022`.

Input:

```text
2147483647 9
```

Expected standard output:

```text
2147483647
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Two's-complement addition overflows exactly under the two sign-change cases tested. The selected bound is the required saturation direction; absent overflow, the 32-bit sum represents the mathematical result.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Evaluating `a+b` as signed C before checking is undefined on overflow. Opposite-sign operands cannot overflow and should not be clamped.
