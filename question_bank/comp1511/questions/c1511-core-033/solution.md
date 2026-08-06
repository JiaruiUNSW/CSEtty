# Alphabet Histogram — solution

## Approach

Scan the string to increment one frequency per character, then scan indices zero through twenty-five to print positive counts and count distinct entries.

## Correctness

Each input character increments exactly its corresponding alphabet bin, so all frequencies are exact. The ordered bin scan prints every positive bin exactly once in alphabetic order.

## Complexity

O(L + 26) time and O(L + 26) storage including the input.

## Common pitfalls

Do not print zero-count letters, reset the frequency array to zero, and convert indices back to letters correctly. Verify boundary inputs as well as the worked example.

