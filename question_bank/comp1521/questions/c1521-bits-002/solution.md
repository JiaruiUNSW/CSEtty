# Extract the Packet High Byte — worked solution

## Idea in one sentence

Use masks and unsigned shifts to implement extract the packet high byte without string conversion.

## Exact rule

Return bits 31 through 24 of `x` as an unsigned value from 0 to 255; ignore `y` and `k`.

## Approach

Use masks and unsigned shifts to implement extract the packet high byte without string conversion. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Parse the two words as unsigned hexadecimal values.
2. Construct each mask from the documented field width.
3. Shift only unsigned values and combine disjoint fields with bitwise operators.
4. Print the final 32-bit pattern with fixed width.

## Worked example

Command arguments: `(no command-line arguments)`

Input:

```text
12345678 00ff00ff 8
```

Output:

```text
result: 00000012
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

Each mask retains exactly the bits belonging to its named field, and each shift moves those bits to the required positions. The final OR/XOR therefore contains exactly the specified result bits.

## Complexity

A fixed number of word operations uses `O(1)` time and space; bit-count/reversal variants use exactly 32 iterations.

## Common pitfalls

Signed right shift, a shift count of 32, a missing `u` suffix, or printing decimal instead of eight-digit hexadecimal changes observable behaviour.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
