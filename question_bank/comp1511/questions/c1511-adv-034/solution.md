# Solution: Undoable event journal

## Approach

Maintain a record array mapping categories to counts and a stack array containing one category string per LOG. UNDO pops the stack and decrements the corresponding record.

## Correctness

Each LOG adds one history entry and one matching count, so counts and total match current history. UNDO removes exactly the latest entry and reverses its count. COUNT and TOTAL therefore report the maintained journal state.

## Complexity

Each update or query is `O(r)` for at most r categories; space is `O(r+h)` for records and history.

## Common pitfalls

Undoing the first rather than last event, deleting a zero-count category and changing first-seen lookup assumptions, or changing total on an empty UNDO. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
