# Parenthesis Stream Audit — solution

## Approach

Read one character at a time. Increment depth for `(` and update the maximum; for `)`, decrement when possible or mark invalid. At the end also require depth zero.

## Correctness

Depth always equals unmatched openers in the processed prefix. A negative-required close is detected immediately, and final depth detects leftover openers; the maximum records the largest valid prefix depth.

## Complexity

O(L) time for line length L and O(1) space.

## Common pitfalls

Ignore non-parenthesis characters, preserve a previously invalid state, and check unmatched openers after input ends. Keep the submitted filename and required output format unchanged.

