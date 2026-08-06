# Trim and Collapse Spacing — solution

## Approach

Track whether a non-whitespace character has been written and whether a whitespace run is pending. On a new ordinary character, first emit one pending separator if appropriate, then emit the character.

## Correctness

Leading whitespace is ignored because no text has been written. Every internal run sets one pending flag and emits one separator before the next character; trailing pending whitespace is never emitted.

## Complexity

O(L) time and O(1) additional space.

## Common pitfalls

Treat tabs like spaces, avoid a trailing space, and always print the final newline even for a blank input line. Keep the submitted filename and required output format unchanged.

