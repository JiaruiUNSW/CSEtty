# Pipe-Transferred Weighted Checksum

## Task

Compute `sum((i + 1) * a[i])` with one-based position weights.

## Background

A parent delegates one deterministic reduction to a child. Because post-fork memory is private, the child returns a fixed-width binary result record through a pipe.

## Requirements

Read `n` and `n` integers. The supplied code creates a pipe and forks one child. Complete the child branch so it computes the required value, transfers one `long long`, closes its pipe end, and exits successfully. The parent waits and prints `result: X`.

## Starter code

Complete the marked child-process branch. The supplied code already reads the array, creates the pipe, forks, receives one `long long`, waits for the child, and prints the result.

## Examples

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

Close unused pipe ends immediately, require full record transfer, use `_exit` in the child, and validate `waitpid` status.

## Submission

Submit `c1521_pipeline_005.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
