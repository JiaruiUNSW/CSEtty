# Recursive Directory Count

## Background

A build/archive inspection tool must walk a supplied directory tree. Only real regular files and real directories participate; traversal order must not affect the scalar result.

## Requirements

Accept one root directory, recursively traverse it, and print `result: X` for the metric in the title. The root directory has depth zero and counts as a directory for directory-count questions.

**Exact rule.** Count the supplied root and every real directory recursively below it; regular files do not count.

Submit `c1521_tree_005.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `tree`
Fixture files: tree/src/one.c, tree/build/two.o

Input:

```text
(empty)
```

Output:

```text
result: 3
```

## Implementation notes

Skip `.` and `..`, construct bounded child paths, call `lstat`, and close every opened `DIR *` even on failure.
