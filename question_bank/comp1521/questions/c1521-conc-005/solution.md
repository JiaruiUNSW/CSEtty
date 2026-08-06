# Child-Built Line Index solution

## Approach

The child opens the file and scans bytes while tracking the absolute offset and whether the current byte begins a line. It writes offset zero when the first byte exists, then writes an offset whenever a byte follows a newline. The parent repeatedly reads complete 64-bit values, doubles a dynamic array when full, closes the channel at EOF, and checks the child's exit status before printing.

## Correctness

A non-empty file's first byte starts line one, so zero is emitted once. Every later logical line starts exactly at a byte whose predecessor is newline; the algorithm emits exactly those offsets when that following byte is encountered. A terminal newline has no following byte and therefore creates no emitted start. The parent preserves the pipe order, which is increasing file order.

## Complexity

Scanning takes (O(B)) time for (B) bytes. The parent stores (O(L)) offsets for (L) lines; amortized append time is constant. Pipe traffic is (8L) bytes.

## Common pitfalls

Emitting immediately upon reading a newline invents a line after a final newline. Keeping the parent's write end open prevents EOF. Pipe reads may split a 64-bit value, and assigning `realloc` directly can lose the original pointer on failure.

