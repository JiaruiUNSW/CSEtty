# Maximum File Tree Depth

## Background

A build/archive inspection tool must walk a supplied directory tree. Only real regular files and real directories participate; traversal order must not affect the scalar result.

## Requirements

Accept one root directory, recursively traverse it, and print `result: X` for the metric in the title. The root directory has depth zero and counts as a directory for directory-count questions.

**Exact rule.** The root has depth 0 and a file's depth is the number of containing subdirectories below the root; return the maximum file depth, or 0 if there are no files.

Submit `c1521_tree_003.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `tree`
Fixture files: tree/src/one.c, tree/build/two.o

Input:

```text
(empty)
```

Output:

```text
result: 1
```

## Implementation notes

Skip `.` and `..`, construct bounded child paths, call `lstat`, and close every opened `DIR *` even on failure.
