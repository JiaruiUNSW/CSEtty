# Largest Recursive File Size

## Task

Return the greatest `st_size` among real regular files, or 0 when the tree contains none.

## Background

A build/archive inspection tool must walk a supplied directory tree. Only real regular files and real directories participate; traversal order must not affect the scalar result.

## Requirements

Accept one root directory, recursively traverse it, and print the computed value as `result: X` followed by one newline. The root directory has depth zero and counts as a directory for directory-count questions. Ignore any file named `.keep`; it is used only to create an otherwise empty test directory.

## Starter code

Complete `static int walk(const char *path, int depth, struct summary *s)`. The supplied `main` initialises the summary and prints the field needed by this question.

## Examples

Command-line arguments: `tree`

Files provided for this example:

- `tree/src/one.c` contains:

  ```text
  int x;
  ```
- `tree/build/two.o` contains:

  ```text
  1234
  ```

Output:

```text
result: 7
```

## Implementation notes

Skip `.` and `..`, construct bounded child paths, call `lstat`, and close every opened `DIR *` even on failure.

## Submission

Submit `c1521_tree_006.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
