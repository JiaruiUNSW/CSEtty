# Append a dynamic checksum

## Background

`int append_checksum(int **values, size_t *length)` grows a heap array by one element containing the sum of all original elements.

## Requirements

- For an empty array, append the checksum zero.
- Update both caller-owned outputs only after successful `realloc`; return 1 on success and 0 on allocation failure.
- The supplied `main` prints the grown array and frees the final pointer.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_024 1 2 3
```

Output:

```text
1 2 3 6
```

## Implementation notes

Assume the checksum and allocation-size calculation fit their types. Use a temporary pointer for `realloc`. Submit `c1511_adv_024.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
