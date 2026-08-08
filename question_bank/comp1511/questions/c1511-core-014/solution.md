# Descending Number Fence — solution

## Approach

Loop from n down through one, print the current value, and print `>` only when the current value is greater than one.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `four`, runs `./c1511_core_014`.

Input:

```text
4
```

Expected standard output:

```text
4>3>2>1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The loop visits every integer from n to one exactly once in descending order. Its separator condition is true precisely between consecutive outputs, so formatting is exact.

## Complexity

O(n) time and O(1) space.

## Common pitfalls

Avoid a trailing separator and remember the final newline. The case n equals one still prints one value. Keep the submitted filename and required output format unchanged.
