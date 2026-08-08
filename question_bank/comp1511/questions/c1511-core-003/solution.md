# Cyclic Trail Distance — solution

## Approach

For every index i, select `(i + 1) % n`, add the absolute label difference, and return the accumulated sum.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `mixed`, runs `./c1511_core_003`.

Input:

```text
4
1 4 2 6
```

Expected standard output:

```text
distance: 14
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each of the n trail edges begins at exactly one index i and ends at its modulo successor. The loop adds each defined edge cost exactly once, hence returns the required total.

## Complexity

O(n) time and O(n) space for the input array.

## Common pitfalls

Do not omit the closing edge, and take the absolute difference rather than a signed difference. Also check every `scanf` target and preserve the required output format.
