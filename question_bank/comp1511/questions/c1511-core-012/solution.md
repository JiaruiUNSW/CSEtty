# Shifted Signal Mismatches — solution

## Approach

For every B index i, calculate the corresponding rotated A index `(i + shift) % n`, compare the values, and count differences.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `perfect-rotation`, runs `./c1511_core_012`.

Input:

```text
4 1
1 2 3 4
2 3 4 1
```

Expected standard output:

```text
mismatches: 0
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The formula selects exactly the element appearing at position i after the defined left rotation. Since all n positions are compared once, the mismatch count is exact.

## Complexity

O(n) time and O(n) space for the two input signals.

## Common pitfalls

Apply the shift in the stated direction, wrap with modulo, and compare with B at the unshifted index. Also check every `scanf` target and preserve the required output format.
