# Most Improved Student — solution

## Approach

Read all records, select the first as current best, and replace it when a later record has a larger gain or wins the stated tie breakers.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `after-breaks-tie`, runs `./c1511_core_032`.

Input:

```text
3
42 60 75
17 70 85
99 50 64
```

Expected standard output:

```text
student: 17
gain: 15
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The comparison helper exactly implements the ordered ranking keys. Maintaining the best record over each scanned prefix therefore yields the unique required winner after the final record.

## Complexity

O(n) time and O(n) space.

## Common pitfalls

Subtract before from after, apply tie breakers in order, and do not use zero as an initial best gain. Verify boundary inputs as well as the worked example.
