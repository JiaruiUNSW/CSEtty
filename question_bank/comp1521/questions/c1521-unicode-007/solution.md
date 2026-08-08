# Unicode Plane Number — worked solution

## Idea in one sentence

Classify the scalar range first, then derive unicode plane number from the UTF-8/UTF-16 boundary table.

## Exact rule

Return `cp >> 16` for a Unicode scalar (planes 0 through 16), or -1 for a non-scalar.

## Approach

Classify the scalar range first, then derive unicode plane number from the UTF-8/UTF-16 boundary table. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Reject non-scalars, including the surrogate interval.
2. Select the encoding width from inclusive boundary values.
3. Build any requested leading/continuation fields with masks.
4. Return the exact integer result.

## Worked example

Input:

```text
000020ac
```

Output:

```text
result: 0
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

The scalar ranges are disjoint and cover every valid code point. Each branch applies the encoding formula for that range, so the returned width/byte/classification is exact.

## Complexity

A constant number of comparisons and shifts uses `O(1)` time and space.

## Common pitfalls

Do not accept surrogates, use `<` where an inclusive boundary needs `<=`, or confuse a code point with an already encoded byte.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
