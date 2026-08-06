# Solution: Resizable integer console

## Approach

Represent data with pointer, length, and capacity. Implement safe geometric `realloc`, stack removal, three-reversal rotation, and an in-place quadratic first-occurrence compaction.

## Correctness

PUSH maintains all prior elements and adds one at the end; DROP removes exactly that end. Three reversals implement the requested rotation. UNIQUE writes precisely first occurrences in encounter order. Sequential dispatch therefore maintains the specified buffer.

## Complexity

PUSH is amortized `O(1)`, DROP `O(1)`, ROLL and PRINT `O(n)`, UNIQUE `O(n^2)`, and storage `O(n)`.

## Common pitfalls

Losing the old pointer on failed realloc, taking modulo by zero, using unsigned indices that underflow, or keeping later rather than first duplicates. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
