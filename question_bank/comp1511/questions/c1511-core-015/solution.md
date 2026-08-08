# Signal State Advances — solution

## Approach

Convert the input character to an enum, repeat the enum transition the requested number of times, then convert the final enum back to its character.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `one-step`, runs `./c1511_core_015`.

Input:

```text
R 1
```

Expected standard output:

```text
state: G
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each loop iteration applies exactly one transition of the specified cycle. By induction on the number of iterations, the enum after `steps` iterations is the required final state.

## Complexity

O(steps) time and O(1) space.

## Common pitfalls

The cycle order is R to G to A to R, and zero steps must leave the state unchanged. Keep the submitted filename and required output format unchanged.
