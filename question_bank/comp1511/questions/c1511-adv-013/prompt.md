# Rotate a heap array left

## Background

This original exercise focuses on safe pointer-based processing of dynamically allocated arrays. `void rotate_left(int *values, size_t length, size_t amount)` rotates the array left by `amount` positions in place. The supplied executable converts command-line text into heap arrays so the function is self-contained and repeatable.

## Requirements

- The first command-line value is the nonnegative rotation amount; remaining values form the array.
- For nonempty arrays, amounts larger than the length wrap using modulo; empty arrays remain empty.
- Use `O(1)` auxiliary storage in the target function and preserve every value.
- Successful output is one space-separated line, or `EMPTY` when the logical result length is zero.

## Examples

`./c1511_adv_013 2 1 2 3 4 5` prints `3 4 5 1 2`; amount 7 on `1 2 3` prints `2 3 1`.

## Implementation notes

The harness allocates the input array and frees it after printing. A three-reversal method is suitable. Submit `c1511_adv_013.c`. Assume all input text represents valid decimal integers within the `int` range. Keep the provided harness and output format unchanged, and compile the unique submission file with `dcc -Werror`.
