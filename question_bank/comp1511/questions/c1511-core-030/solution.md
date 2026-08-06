# Line Initials — solution

## Approach

Read the line, track whether the preceding position is inside a word, and on each transition from separator to non-separator append the uppercase initial and increment the word count.

## Correctness

Every word has exactly one separator-to-word transition at its first character, and no other character has such a transition. Therefore the algorithm appends exactly one correct initial per word.

## Complexity

O(L) time and O(L) space for a line of length L.

## Common pitfalls

Treat tabs as separators, avoid reading beyond the null terminator, and handle leading, trailing, or all-separator lines. Verify boundary inputs as well as the worked example.

