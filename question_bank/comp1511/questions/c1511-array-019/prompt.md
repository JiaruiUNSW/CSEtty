# Archive Position Checksum

## Background

The data in a numbered archive shelf arrives as a bounded integer array. A small, auditable metric is needed before the next processing stage.

## Requirements

Read `n` (0 to 100), followed by `n` signed integers. Compute the metric named in the title and print `result: X` followed by a newline. Empty input arrays use the neutral result shown by the public test.

**Exact rule.** Compute `sum((i + 1) * a[i])` using one-based position weights.

Submit `c1511_array_019.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
result: 2
```

## Implementation notes

Use an array and a helper function. Do not sort or alter the input unless the metric explicitly depends on ordering. All supplied arithmetic fits in `long long`.
