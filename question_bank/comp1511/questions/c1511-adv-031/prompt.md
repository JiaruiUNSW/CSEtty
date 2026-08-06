# Repair the frequency allocation

## Background

This original medium exercise combines several C concepts in one self-contained linked or dynamically allocated data task. `size_t *make_frequencies(const int *values, size_t length, size_t maximum)` allocates a zero-initialised table for keys 0 through `maximum` and counts each input. The supplied harness constructs all input state and retains the ownership rules described below.

## Requirements

- The first command-line value is `maximum`; every remaining value is guaranteed in range.
- Return a table of exactly `maximum + 1` counters owned by the caller.
- The starter's uninitialised allocation is the bug; fix it without changing output format.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

`./c1511_adv_031 4 1 3 1` prints `1=2 3=1`; no observed values print `EMPTY`.

## Implementation notes

The printer omits zero-frequency keys. Use a portable allocation that guarantees zeroed counters. Submit `c1511_adv_031.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source. The build uses the shell-free argument array `dcc -Werror <file> -o <program>`.
