# Solution: Recursive character tally

## Approach

Return zero at the terminator. Otherwise add whether the current byte equals the target to the recursive count of the suffix.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `basic`, runs `./c1511_adv_023 a banana`.

Input:

```text
(empty)
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The base case correctly counts the empty suffix. Assuming recursion counts the suffix, adding the current byte's match indicator gives the exact count for the whole current string.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Recursing without advancing, counting the terminator, or comparing strings rather than individual characters. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
