# Compact neighbouring repeats

## Background

`size_t compact_runs(int *values, size_t length)` removes adjacent duplicate values in place and returns the new logical length. The supplied executable converts command-line text into heap arrays so the function is self-contained and repeatable.

## Requirements

- Keep exactly the first value of each maximal equal run.
- Do not allocate memory or change the relative order of retained values.
- Only the first returned-length elements matter; empty input returns zero.
- Successful output is one space-separated line, or `EMPTY` when the logical result length is zero.

## Examples

Command:

```text
./c1511_adv_014 1 1 2 2 2 3
```

Output:

```text
1 2 3
```

## Implementation notes

Use separate read and write positions. The supplied `main` still frees the original allocation after printing the logical prefix. Submit `c1511_adv_014.c`. Assume all input text represents valid decimal integers within the `int` range. Keep the provided starter program and output format unchanged.
