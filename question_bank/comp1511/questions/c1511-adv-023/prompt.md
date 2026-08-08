# Recursive character tally

## Background

`size_t recursive_tally(const char *text, char target)` recursively counts occurrences of one byte in a null-terminated string.

## Requirements

- The first argument must contain exactly one target character; the second is the text.
- Use recursion for the traversal and do not call string-search or counting library functions.
- The empty string returns zero and matching is case-sensitive.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_023 a banana
```

Output:

```text
3
```

## Implementation notes

Use the null terminator as the base case and add either zero or one before the recursive result. Submit `c1511_adv_023.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
