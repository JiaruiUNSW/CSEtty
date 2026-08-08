# Temperature Drift — solution

## Approach

Calculate end minus start once, select a direction from its sign, and print both fields.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `rise`, runs `./c1511_core_020`.

Input:

```text
12 17
```

Expected standard output:

```text
change: 5
direction: rising
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The difference formula gives the required signed change. Positive, negative, and zero are exhaustive and mutually exclusive, so the selected direction is correct.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Preserve the sign by subtracting start from end, and spell the three labels exactly. Keep the submitted filename and required output format unchanged.
