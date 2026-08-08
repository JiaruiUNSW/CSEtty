# Triangle Label — solution

## Approach

Reject if any inequality fails, otherwise test all-three equality, then any pair equality, and use scalene as the remaining case.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `isosceles`, runs `./c1511_core_027`.

Input:

```text
5 5 8
```

Expected standard output:

```text
triangle: isosceles
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The rejection predicate is exactly the negation of the strict triangle inequalities. Among valid triangles, the ordered equality tests partition cases into three equal, exactly two equal, and none equal.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

A sum equal to the third side is invalid. Check every side ordering and test invalidity before equality labels. Keep the submitted filename and required output format unchanged.
