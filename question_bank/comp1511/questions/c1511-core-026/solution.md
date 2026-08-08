# Repair the Clock Wrap — solution

## Approach

Convert the input to total minutes, add the offset, reduce modulo 1440, normalise a negative result, then divide and take remainder by 60.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `forward`, runs `./c1511_core_026`.

Input:

```text
10 30 45
```

Expected standard output:

```text
11:15
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Times differing by multiples of 1440 represent the same time of day. Normalisation selects its unique total in zero through 1439, whose quotient and remainder by 60 are the correct hour and minute.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Do not use modulo 24 on a minute total, and correct negative remainder before calculating the fields. Keep the submitted filename and required output format unchanged.
