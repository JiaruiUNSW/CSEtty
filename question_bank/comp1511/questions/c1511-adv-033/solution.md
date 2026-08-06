# Solution: Component stock ledger

## Approach

Store records in a fixed array of structures. A linear lookup supports both update and rejection. Process commands until END; SHOW scans the array in insertion order and skips zero quantities.

## Correctness

ADD either updates the unique matching record or appends one, so quantities equal total additions minus accepted takes. TAKE changes a quantity exactly when sufficient. SHOW visits all records in first-seen order and emits precisely positive ones, with the required empty and terminator rules.

## Complexity

With r records and c commands, `O(cr)` time and `O(r)` fixed record space.

## Common pitfalls

Creating a record for a rejected TAKE, allowing quantities to become negative, omitting the SHOW terminator, or sorting records. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
