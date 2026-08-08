# Row Champion — solution

## Approach

Compute sum and range for row zero, then scan later rows. Replace the champion on a larger sum or on an equal sum with a smaller range; leave exact ties unchanged.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `sum-wins`, runs `./c1511_core_031`.

Input:

```text
3 3
1 2 3
4 0 2
-1 10 -1
```

Expected standard output:

```text
row: 2
sum: 8
range: 11
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After processing each prefix of rows, the stored champion is best under the lexicographic rules because it is updated exactly when the new row outranks it. Induction yields the global champion.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Do not initialise the best sum to zero, apply range only after a sum tie, and retain the earlier index for a complete tie. Verify boundary inputs as well as the worked example.
