# Alphabet Histogram — solution

## Approach

Scan the string to increment one frequency per character, then scan indices zero through twenty-five to print positive counts and count distinct entries.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `banana`, runs `./c1511_core_033`.

Input:

```text
banana
```

Expected standard output:

```text
a: 3
b: 1
n: 2
distinct: 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each input character increments exactly its corresponding alphabet bin, so all frequencies are exact. The ordered bin scan prints every positive bin exactly once in alphabetic order.

## Complexity

O(L + 26) time and O(L + 26) storage including the input.

## Common pitfalls

Do not print zero-count letters, reset the frequency array to zero, and convert indices back to letters correctly. Verify boundary inputs as well as the worked example.
