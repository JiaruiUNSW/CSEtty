# Same-Day Elapsed Minutes — solution

## Approach

Store both times in structs, map each to `hour * 60 + minute`, and subtract the start total from the finish total.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `normal`, runs `./c1511_core_023`.

Input:

```text
9 45 11 10
```

Expected standard output:

```text
elapsed: 85 minutes
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The conversion counts exact minutes since midnight. Because both times are on the same day, subtracting those positions gives precisely the elapsed duration.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Do not subtract hours and minutes independently without borrowing. Equal times yield zero. Keep the submitted filename and required output format unchanged.
