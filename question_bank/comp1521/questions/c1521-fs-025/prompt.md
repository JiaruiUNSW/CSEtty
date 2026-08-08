# Recursive per-directory usage

## Background

A storage report may distinguish bytes held directly in each directory from descendant totals. Stable relative paths make such reports comparable across runs.

## Requirements

- Write `c1521_fs_025.c`.
- Recursively traverse the root without following symlinks.
- Print one line for every real directory, including root, containing `RELATIVE_PATH BYTES`; `BYTES` is the sum of sizes of regular files immediately in that directory only.
- Represent root as `.`, use `/` separators, include zero-byte totals, and globally sort paths by `strcmp`.
- Ignore other object types.
- Any failure prints `c1521_fs_025: error\n` to standard error and returns 1.

## Examples

Command:

```text
./c1521_fs_025 tree
```

Files provided for this example:

- `tree/a` (3 bytes) contains:

  ```text
  aa
  ```
- `tree/sub/b` (4 bytes) contains:

  ```text
  bbb
  ```

Output:

```text
. 3
sub 4
```

## Implementation notes

Use `opendir`, `readdir`, and `lstat` with dynamic paths and records. Do not roll descendant bytes into ancestors, use `chdir`, follow symlinks, or invoke `du`. Submit `c1521_fs_025.c`.
