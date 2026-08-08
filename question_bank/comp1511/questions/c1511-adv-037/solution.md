# Solution: Resizable integer console

## Approach

Represent data with pointer, length, and capacity. Implement safe geometric `realloc`, stack removal, three-reversal rotation, and an in-place quadratic first-occurrence compaction.


## Step-by-step

1. Draw the empty, one-node, and general cases before changing any links.
2. Save each pointer that will still be needed, then update or recurse using the invariant above.
3. Make ownership explicit: every retained node stays reachable and every removed allocation is freed once.
4. Return the possibly changed head and test the boundary cases before longer lists.

## Worked example

The first public test, `basic`, runs `./c1511_adv_037`.

Input:

```text
PUSH 1
PUSH 2
PUSH 3
ROLL 1
PRINT
END
```

Expected standard output:

```text
3 1 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

PUSH maintains all prior elements and adds one at the end; DROP removes exactly that end. Three reversals implement the requested rotation. UNIQUE writes precisely first occurrences in encounter order. Sequential dispatch therefore maintains the specified buffer.

## Complexity

PUSH is amortized `O(1)`, DROP `O(1)`, ROLL and PRINT `O(n)`, UNIQUE `O(n^2)`, and storage `O(n)`.

## Common pitfalls

Losing the old pointer on failed realloc, taking modulo by zero, using unsigned indices that underflow, or keeping later rather than first duplicates. Also consume each command's complete arguments, keep output spelling and line breaks exact, and ensure cleanup remains correct after empty-state and repeated-operation cases.
