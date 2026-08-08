# Unique merge of two sorted arrays

## Background

`int *merge_unique(...)` creates a sorted union of two nondecreasing arrays and reports its length. The supplied executable converts command-line text into heap arrays so the function is self-contained and repeatable.

## Requirements

- Command-line values before `--` form the first array and values after it form the second; both may be empty.
- Remove duplicates both within and across arrays while preserving sorted order.
- Allocate at most `left_length + right_length` integers and do not modify either input.
- Successful output is one space-separated line, or `EMPTY` when the logical result length is zero.

## Examples

Command:

```text
./c1511_adv_016 1 3 5 -- 2 3 4
```

Output:

```text
1 2 3 4 5
```

## Implementation notes

Use two read indices and one write index. Exactly one `--` delimiter is guaranteed. The caller frees all three arrays. Submit `c1511_adv_016.c`. Assume all input text represents valid decimal integers within the `int` range. Keep the provided starter program and output format unchanged.
