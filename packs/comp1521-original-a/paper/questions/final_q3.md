# Q3 — Count logical lines with POSIX file I/O

## Background

Text tools normally regard each newline byte as ending a line, but a non-empty
file whose final byte is not a newline still has a final logical line. Programs
that stream a file in blocks must remember enough state across `read` calls to
handle that case correctly.

## Program requirements

Complete `final_q3.c`. The program is invoked with exactly one pathname and
must:

- open that path read-only with `open(2)`;
- read the file using `read(2)` until EOF;
- count every newline byte;
- add one more logical line when the file is non-empty and its final byte is not
  a newline;
- print the count followed by a newline; and
- close the descriptor on the successful path.

Do not use `fopen`, `fgets`, `getc`, `mmap`, `system`, or another process. Return
a non-zero status if the argument count is wrong, the file cannot be opened, or
a read fails. An empty file contains zero logical lines.

## Examples

For a file containing `alpha\nbeta\n`:

```text
$ ./final_q3 input.txt
2
```

For a file containing `alpha\nbeta` with no final newline, the output is also:

```text
2
```

## Implementation notes

Read into a fixed-size byte buffer. Track the total number of bytes read and the
last byte seen; do not assume one call to `read` returns the whole file.

