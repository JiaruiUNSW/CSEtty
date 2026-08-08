# Trim and Collapse Spacing — solution

## Approach

Track whether a non-whitespace character has been written and whether a whitespace run is pending. On a new ordinary character, first emit one pending separator if appropriate, then emit the character.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `spaces`, runs `./c1511_core_024`.

Input:

```text
  hello   world
```

Expected standard output:

```text
hello world
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Leading whitespace is ignored because no text has been written. Every internal run sets one pending flag and emits one separator before the next character; trailing pending whitespace is never emitted.

## Complexity

O(L) time and O(1) additional space.

## Common pitfalls

Treat tabs like spaces, avoid a trailing space, and always print the final newline even for a blank input line. Keep the submitted filename and required output format unchanged.
