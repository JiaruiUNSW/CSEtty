# Solution: Repair running differences

## Approach

Save the original element zero. For each later index, save the current original, write current minus saved previous, then update the saved previous.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `basic`, runs `./c1511_adv_019 5 9 12`.

Input:

```text
(empty)
```

Expected standard output:

```text
5 4 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Before each iteration the saved value is the original predecessor. The assignment therefore writes the specified difference, and saving the current original before overwriting establishes the invariant for the next index.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Subtracting an already transformed predecessor, starting at index zero, or allocating an unnecessary copy. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
