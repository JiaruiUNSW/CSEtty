# Repair the frequency allocation

## Background

`size_t *make_frequencies(const int *values, size_t length, size_t maximum)` allocates a zero-initialised table for keys 0 through `maximum` and counts each input.

## Requirements

- The first command-line value is `maximum`; every remaining value is guaranteed in range.
- Return a table of exactly `maximum + 1` counters owned by the caller.
- The starter's uninitialised allocation is the bug; fix it without changing output format.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

Command:

```text
./c1511_adv_031 4 1 3 1
```

Output:

```text
1=2 3=1
```

## Implementation notes

The printer omits zero-frequency keys. Use a portable allocation that guarantees zeroed counters. Submit `c1511_adv_031.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source.
