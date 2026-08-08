# Repair the Range Clamp — solution

## Approach

Compare the value with the lower bound first and return lower when needed; compare it with upper and return upper when needed; otherwise return the original value.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `above`, runs `./c1511_core_019`.

Input:

```text
0 10 14
```

Expected standard output:

```text
clamped: 10
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The three branches partition all integers into below, inside, and above the interval. Each branch returns exactly the value required for its partition.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Do not swap lower and upper returns, use strict comparisons so boundary values remain unchanged, and ensure every path returns. Keep the submitted filename and required output format unchanged.
