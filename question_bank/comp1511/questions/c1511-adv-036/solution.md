# Solution: Reversible marker chain

## Approach

Implement head insertion, tail insertion, pointer-to-pointer first removal, iterative reversal, printing, and destruction as separate helpers. Dispatch commands in a read loop.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_036`.

Input:

```text
APPEND red
APPEND blue
PREPEND green
PRINT
END
```

Expected standard output:

```text
green -> red -> blue
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each helper performs exactly its named local link update while preserving every unaffected node. Command dispatch applies helpers in input order, so PRINT observes the specified current chain; destruction frees every final node.

## Complexity

PREPEND is `O(1)`; APPEND, REMOVE, REVERSE, PRINT, and final destruction are `O(n)`; heap space is `O(n)`.

## Common pitfalls

Losing the old head during reversal, deleting all duplicates rather than the first, not updating head on front removal, or omitting final cleanup. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
