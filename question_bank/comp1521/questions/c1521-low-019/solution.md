# Rotate a 32-Bit Word — solution guide

## Approach

Return the input when the count is zero; otherwise OR the left-shifted body with the high bits wrapped down by the complementary shift.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `wrap`, runs `./c1521_low_019`.

Input:

```text
80000001 1
```

Expected standard output:

```text
00000003
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every original bit moves `k` positions modulo 32: bits that remain in range come from the left shift, and wrapped bits come from the right shift. The disjoint pieces OR to the rotation.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Signed right shift is implementation-defined for negatives. Never evaluate `value >> 32` in the zero-count case.
