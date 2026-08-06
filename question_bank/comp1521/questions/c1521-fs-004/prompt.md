# Select a numbered line

## Background

Text streams can contain lines of arbitrary length. This exercise asks for a streaming line selector that never needs to retain a whole file or seek backwards.

## Requirements

Write `c1521_fs_004.c`. Run it with a filename and a positive, one-based line number. Copy exactly that logical line to standard output. If the selected final line lacks a newline, add one. If the file has too few lines, print `NOT FOUND\n`. Invalid arguments or a file error print `c1521_fs_004: error\n` to standard error and return 1; selection or `NOT FOUND` returns 0.

## Examples

For lines `red`, `green`, `blue`, selecting line 2 prints `green`. Selecting line 8 prints `NOT FOUND`.

## Implementation notes

Use standard I/O (`fopen` and `fgetc` are sufficient). A line ends at newline or EOF, and an empty file has zero lines. Do not use a fixed-size line buffer, `getline`, `sed`, or `awk`. Submit `c1521_fs_004.c`.
