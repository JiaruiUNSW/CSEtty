# Worked solution — Q3

## Approach

Stream the file through a fixed-size buffer. Add one for each newline byte,
record the final byte of every non-empty chunk, and count the total bytes read.
After EOF, add one only when at least one byte was read and the last byte was
not a newline.

## Correctness

Every file byte appears in exactly one returned `read` chunk, so the nested scan
counts every newline exactly once. Each newline terminates one logical line. If
the non-empty file ends without a newline, precisely one remaining sequence of
bytes follows the last newline and represents one additional logical line. The
final condition adds exactly that line and adds none for an empty or
newline-terminated file.

## Complexity

For a file of n bytes, time is O(n) and auxiliary space is O(1) because the
buffer size is fixed.

## Common pitfalls

- Counting only newline bytes and missing an unterminated final line.
- Treating an empty file as one line.
- Assuming `read` fills the buffer or returns the whole file.
- Ignoring `read < 0` or leaking the file descriptor.

