# Restock Manifest — solution

## Approach

Read all item structs, then scan them once. For each, compute `target - current` when positive, print positive needs, and add them to the total.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `mixed`, runs `./c1511_core_029`.

Input:

```text
3
101 5 8
102 10 7
103 0 2
```

Expected standard output:

```text
101: 3
103: 2
total needed: 5
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The helper returns exactly the missing quantity for below-target items and zero otherwise. The scan visits every item once in input order, so all required lines and the summed total are exact.

## Complexity

O(n) time and O(n) space.

## Common pitfalls

Do not print items exactly at target, never add a negative need, and keep the final summary even when no item needs stock. Verify boundary inputs as well as the worked example.
