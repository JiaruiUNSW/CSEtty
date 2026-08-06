# Copy values inside a gate

## Background

This original exercise focuses on safe pointer-based processing of dynamically allocated arrays. `int *copy_in_range(const int *values, size_t length, int low, int high, size_t *result_length)` allocates an exact-size array containing values in the inclusive range. The supplied executable converts command-line text into heap arrays so the function is self-contained and repeatable.

## Requirements

- The first two command-line arguments are `low` and `high`, with `low <= high`; remaining arguments form the input array.
- Preserve order, set `*result_length`, and return `NULL` when no value qualifies.
- Allocate no more elements than the result needs and leave the input unchanged.
- Successful output is one space-separated line, or `EMPTY` when the logical result length is zero.

## Examples

`./c1511_adv_015 2 5 1 2 5 7` prints `2 5`; a range with no qualifying values prints `EMPTY`.

## Implementation notes

A count pass followed by a copy pass is expected. The caller frees the returned pointer, including safely calling `free(NULL)`. Submit `c1511_adv_015.c`. Assume all input text represents valid decimal integers within the `int` range. Keep the provided harness and output format unchanged, and compile the unique submission file with `dcc -Werror`.
