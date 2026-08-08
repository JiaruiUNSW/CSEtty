# Count Echo Valleys — solution

## Approach

Read the sequence, then visit each interior index and increment a counter exactly when both strict less-than comparisons succeed.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `two-valleys`, runs `./c1511_core_001`.

Input:

```text
5
4 1 3 2 5
```

Expected standard output:

```text
valleys: 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

For every possible interior index, the loop checks precisely the two inequalities in the definition. It increments once for each valley and never for a non-valley, so the final counter is exact.

## Complexity

The scan takes O(n) time and the stored array uses O(n) space.

## Common pitfalls

Do not inspect outside the array, count endpoints, or treat equal adjacent values as a strict valley. Also check every `scanf` target and preserve the required output format.
