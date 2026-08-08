# Classify a filesystem object

## Background

The `stat` system call reports both an object's type and, for regular files, its byte length. Correct code uses the `S_IS...` macros rather than comparing raw mode bits by eye.

## Requirements

- Write `c1521_fs_003.c`.
- It receives exactly one path.
- If the path names a regular file, print `regular SIZE`; if it names a directory, print `directory`; for every other successfully stated type, print `other`.
- End the line with a newline.
- If arguments are wrong or `stat` fails, print `c1521_fs_003: error\n` to standard error and return 1.
- Successful classification returns 0.

## Examples

Command:

```text
./c1521_fs_003 item
```

Files provided for this example:

- `item` (4 bytes) contains:

  ```text
  abc
  ```

Output:

```text
regular 4
```

## Implementation notes

Use `stat`, `S_ISREG`, and `S_ISDIR`. Follow symbolic links as ordinary `stat` does. Do not open or read the object's contents and do not invoke `ls`, `find`, or `wc`. Submit `c1521_fs_003.c`.
