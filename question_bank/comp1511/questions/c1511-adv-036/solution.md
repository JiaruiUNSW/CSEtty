# Solution: Reversible marker chain

## Approach

Implement head insertion, tail insertion, pointer-to-pointer first removal, iterative reversal, printing, and destruction as separate helpers. Dispatch commands in a read loop.

## Correctness

Each helper performs exactly its named local link update while preserving every unaffected node. Command dispatch applies helpers in input order, so PRINT observes the specified current chain; destruction frees every final node.

## Complexity

PREPEND is `O(1)`; APPEND, REMOVE, REVERSE, PRINT, and final destruction are `O(n)`; heap space is `O(n)`.

## Common pitfalls

Losing the old head during reversal, deleting all duplicates rather than the first, not updating head on front removal, or omitting final cleanup. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
