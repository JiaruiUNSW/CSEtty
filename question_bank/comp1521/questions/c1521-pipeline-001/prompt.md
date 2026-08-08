# Pipe-Transferred Child Sum

## Background

A parent delegates one deterministic reduction to a child. Because post-fork memory is private, the child returns a fixed-width binary result record through a pipe.

## Requirements

Read `n` and `n` integers, create a pipe, fork one child to compute the title's metric, transfer one `long long`, wait successfully, and print `result: X`.

**Exact rule.** Return the sum of all input elements, or 0 for an empty array.

Submit `c1521_pipeline_001.c`. Your program must not print prompts or explanatory text.

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

Close unused pipe ends immediately, require full record transfer, use `_exit` in the child, and validate `waitpid` status.
