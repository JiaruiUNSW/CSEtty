# Solution: Labelled reading summaries

## Approach

Use an array of summary structures and linear lookup. Initialize all four aggregates on a first READ; otherwise update count, sum, min, and max. RESET shifts later structures left.

## Correctness

Each summary field is initialized from its first reading and updated by the defining aggregate rule for every later reading. STATS therefore reports exact aggregates. RESET removes exactly the named record while retaining all others.

## Complexity

`O(cr)` time for c commands over at most r summaries and `O(r)` space.

## Common pitfalls

Initializing minimum or maximum to zero, dividing before checking existence, forgetting to shift all structure fields on RESET, or using floating-point output. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
