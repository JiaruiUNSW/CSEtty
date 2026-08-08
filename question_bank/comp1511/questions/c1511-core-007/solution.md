# Warm Cross Centres — solution

## Approach

Visit every non-border cell, calculate the four-neighbour sum, compare it with four times the centre, and increment the result when strict inequality holds.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `hot-centre`, runs `./c1511_core_007`.

Input:

```text
3 3
0 0 0
0 5 0
0 0 0
```

Expected standard output:

```text
warm centres: 1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The nested loops visit every eligible interior cell exactly once. The integer inequality is algebraically equivalent to centre greater than neighbour average, so each visit is classified exactly.

## Complexity

O(rows * columns) time and O(rows * columns) space.

## Common pitfalls

Do not read neighbours for border cells. Equality is not warm, and diagonal cells are not neighbours. Also check every `scanf` target and preserve the required output format.
