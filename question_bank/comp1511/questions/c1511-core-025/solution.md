# Character Run Count — solution

## Approach

Initialise the count to one and scan from index one, incrementing whenever the current character differs from the previous character.

## Correctness

The first character starts the first run. Every remaining run starts at exactly a position where adjacent characters differ, so counting those boundaries plus one gives the exact number.

## Complexity

O(L) time and O(L) input storage.

## Common pitfalls

Do not count individual repeated characters as separate runs, and begin the scan at the second character. Keep the submitted filename and required output format unchanged.

