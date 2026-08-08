# Alternating Digit Score — solution

## Approach

Repeatedly take value modulo ten, add or subtract it according to a toggled sign, then divide value by ten until no digits remain.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `five-digits`, runs `./c1511_core_021`.

Input:

```text
12345
```

Expected standard output:

```text
score: 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At iteration k, remainder extracts exactly the kth digit from the right and the toggled sign matches the alternating definition. Every digit is processed once.

## Complexity

O(D) time for D digits and O(1) space.

## Common pitfalls

The rightmost digit is added, not subtracted. Ensure input zero produces score zero. Keep the submitted filename and required output format unchanged.
