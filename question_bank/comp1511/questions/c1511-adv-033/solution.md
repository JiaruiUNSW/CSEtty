# Solution: Component stock ledger

## Approach

Store records in a fixed array of structures. A linear lookup supports both update and rejection. Process commands until END; SHOW scans the array in insertion order and skips zero quantities.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `basic`, runs `./c1511_adv_033`.

Input:

```text
ADD bolts 5
TAKE bolts 2
SHOW
END
```

Expected standard output:

```text
TAKEN bolts 3
bolts 3
--
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

ADD either updates the unique matching record or appends one, so quantities equal total additions minus accepted takes. TAKE changes a quantity exactly when sufficient. SHOW visits all records in first-seen order and emits precisely positive ones, with the required empty and terminator rules.

## Complexity

With r records and c commands, `O(cr)` time and `O(r)` fixed record space.

## Common pitfalls

Creating a record for a rejected TAKE, allowing quantities to become negative, omitting the SHOW terminator, or sorting records. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
