# Whitespace Group Counter — worked solution

## Idea in one sentence

Scan the line from left to right and retain only the state needed for whitespace group counter.

## Exact rule

Count maximal contiguous groups of whitespace characters.

## Approach

Scan the line from left to right and retain only the state needed for whitespace group counter. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Read the whole line and remove its trailing newline.
2. Initialise counters plus any previous-character or nesting state.
3. Classify each character once and update the state according to the exact rule.
4. Return the scalar result and print it once.

## Worked example

Input:

```text
A1 beta
```

Output:

```text
result: 1
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

The scan classifies every character exactly once. Its counters and previous-state variables describe the processed prefix, and the update matches the definition for the next character. Thus the returned result describes the full line.

## Complexity

The algorithm uses `O(n)` time and `O(1)` auxiliary space, except the normalised-palindrome variant's `O(n)` buffer.

## Common pitfalls

Do not use `scanf("%s")`, count the newline, pass a negative plain `char` to `<ctype.h>`, or forget to validate unmatched closing parentheses.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
