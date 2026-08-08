# Order the endpoint values

## Background

`void order_endpoints(int *first, int *last)` swaps the values addressed by its two pointers only when the first value is greater than the last.

## Requirements

- For arrays of fewer than two values, the supplied `main` does not call the function.
- Do not reorder any interior element.
- Perform the swap through the pointers without indexing the array inside the function.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_017 9 2 4
```

Output:

```text
4 2 9
```

## Implementation notes

The command-line arguments are the array values. The supplied `main` allocates, prints, and frees the array. Submit `c1511_adv_017.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
