# Line Initials — solution

## Approach

Read the line, track whether the preceding position is inside a word, and on each transition from separator to non-separator append the uppercase initial and increment the word count.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `three-words`, runs `./c1511_core_030`.

Input:

```text
hello   wide world
```

Expected standard output:

```text
initials: HWW
words: 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every word has exactly one separator-to-word transition at its first character, and no other character has such a transition. Therefore the algorithm appends exactly one correct initial per word.

## Complexity

O(L) time and O(L) space for a line of length L.

## Common pitfalls

Treat tabs as separators, avoid reading beyond the null terminator, and handle leading, trailing, or all-separator lines. Verify boundary inputs as well as the worked example.
