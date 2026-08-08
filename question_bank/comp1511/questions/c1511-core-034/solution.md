# Busiest Two-by-Two Window — solution

## Approach

Enumerate top rows zero through rows minus two and left columns zero through columns minus two, compute each four-cell sum, and replace the best only on a strict increase.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `bottom-right`, runs `./c1511_core_034`.

Input:

```text
3 3
1 2 0
0 4 1
2 0 3
```

Expected standard output:

```text
top: 1 1
sum: 8
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The loops visit every valid window exactly once. Strict replacement selects the greatest sum while leaving the first row-major window on ties, which implements both tie breakers.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Do not start windows on the last row or column, and do not replace the best on equal sums. Verify boundary inputs as well as the worked example.
