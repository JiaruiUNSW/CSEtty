# Solution: Labelled reading summaries

## Approach

Use an array of summary structures and linear lookup. Initialize all four aggregates on a first READ; otherwise update count, sum, min, and max. RESET shifts later structures left.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `basic`, runs `./c1511_adv_035`.

Input:

```text
READ zone 4
READ zone 8
STATS zone
END
```

Expected standard output:

```text
zone count=2 min=4 max=8 mean=6
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each summary field is initialized from its first reading and updated by the defining aggregate rule for every later reading. STATS therefore reports exact aggregates. RESET removes exactly the named record while retaining all others.

## Complexity

`O(cr)` time for c commands over at most r summaries and `O(r)` space.

## Common pitfalls

Initializing minimum or maximum to zero, dividing before checking existence, forgetting to shift all structure fields on RESET, or using floating-point output. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
