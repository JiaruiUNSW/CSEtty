# Recursive Regular File Count

## Task

Count regular files anywhere below the supplied root. Directories and the reserved `.keep` placeholder do not count.

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
result: 2
```

## Implementation notes

Skip `.` and `..`, construct bounded child paths, call `lstat`, and close every opened `DIR *` even on failure.

## Submission

Submit `c1521_tree_001.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
