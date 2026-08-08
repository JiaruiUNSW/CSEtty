# Diagonal Colour Changes — solution

## Approach

Walk diagonal indices from one to n - 1 and compare grid[i][i] with grid[i - 1][i - 1], counting inequalities.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `two-changes`, runs `./c1511_core_010`.

Input:

```text
4
1 9 9 9
8 1 8 8
7 7 2 7
6 6 6 3
```

Expected standard output:

```text
diagonal changes: 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every consecutive pair on the main diagonal corresponds to exactly one loop index, and the loop counts it exactly when its values differ. Therefore all and only changes are counted.

## Complexity

Reading uses O(n squared) time and space; the diagonal scan itself is O(n).

## Common pitfalls

Do not compare values in the same row or anti-diagonal, and do not count the first diagonal value as a change. Also check every `scanf` target and preserve the required output format.
