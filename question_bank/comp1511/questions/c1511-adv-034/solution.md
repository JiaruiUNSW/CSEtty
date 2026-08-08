# Solution: Undoable event journal

## Approach

Maintain a record array mapping categories to counts and a stack array containing one category string per LOG. UNDO pops the stack and decrements the corresponding record.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `basic`, runs `./c1511_adv_034`.

Input:

```text
LOG rain
LOG wind
LOG rain
COUNT rain
TOTAL
END
```

Expected standard output:

```text
rain 2
TOTAL 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each LOG adds one history entry and one matching count, so counts and total match current history. UNDO removes exactly the latest entry and reverses its count. COUNT and TOTAL therefore report the maintained journal state.

## Complexity

Each update or query is `O(r)` for at most r categories; space is `O(r+h)` for records and history.

## Common pitfalls

Undoing the first rather than last event, deleting a zero-count category and changing first-seen lookup assumptions, or changing total on an empty UNDO. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
