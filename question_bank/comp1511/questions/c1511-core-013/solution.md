# Metro Fare Band — solution

## Approach

Initialise the fare to four, use an if/else-if chain for one distance band, add two if peak is set, and print the result.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `local-offpeak`, runs `./c1511_core_013`.

Input:

```text
4 0
```

Expected standard output:

```text
fare: $4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The chain selects the unique band containing the valid distance and adds its specified surcharge. The final independent condition adds exactly the required peak amount, so the printed fare follows the rule.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Boundary distances 5 and 15 belong to the lower bands. The peak surcharge is in addition to exactly one distance band. Keep the submitted filename and required output format unchanged.
