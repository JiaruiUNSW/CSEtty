# Longest Gentle Climb — solution

## Approach

Start both lengths at one. For every later element, extend the current run when it is at least its predecessor; otherwise restart at one, then update the maximum.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `two-best`, runs `./c1511_core_002`.

Input:

```text
6
1 2 2 0 3 4
```

Expected standard output:

```text
longest: 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The current counter equals the length of the non-decreasing run ending at the current index. Taking the maximum of these exact ending lengths over all indices yields the longest run.

## Complexity

The algorithm runs in O(n) time and stores O(n) input values.

## Common pitfalls

Equality extends a run. Remember that n may be one, and update the maximum after every element. Also check every `scanf` target and preserve the required output format.
