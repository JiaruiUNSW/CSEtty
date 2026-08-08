# Freezer Alarm Count

## Background

The data in a cold-chain sensor feed arrives as a bounded integer array. A small, auditable metric is needed before the next processing stage.

## Requirements

Read `n` (0 to 100), followed by `n` signed integers. Compute the metric named in the title and print `result: X` followed by a newline. Empty input arrays use the neutral result shown by the public test.

**Exact rule.** Count elements strictly less than zero; zero is not negative.

Submit `c1511_array_002.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
result: 3
```

## Implementation notes

Use an array and a helper function. Do not sort or alter the input unless the metric explicitly depends on ordering. All supplied arithmetic fits in `long long`.
