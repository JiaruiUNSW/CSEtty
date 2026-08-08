# Parenthesis Stream Audit — solution

## Approach

Read one character at a time. Increment depth for `(` and update the maximum; for `)`, decrement when possible or mark invalid. At the end also require depth zero.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `nested`, runs `./c1511_core_017`.

Input:

```text
(a(b)c)
```

Expected standard output:

```text
valid: yes
max depth: 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Depth always equals unmatched openers in the processed prefix. A negative-required close is detected immediately, and final depth detects leftover openers; the maximum records the largest valid prefix depth.

## Complexity

O(L) time for line length L and O(1) space.

## Common pitfalls

Ignore non-parenthesis characters, preserve a previously invalid state, and check unmatched openers after input ends. Keep the submitted filename and required output format unchanged.
