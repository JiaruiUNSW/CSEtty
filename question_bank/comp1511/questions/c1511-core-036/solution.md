# Digit-Run Redactor — solution

## Approach

Track whether the scan is currently inside a digit run. Print one marker and increment the count when entering a run; print non-digits normally and clear the state.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `two-runs`, runs `./c1511_core_036`.

Input:

```text
Room 12, shelf 003.
```

Expected standard output:

```text
Room #, shelf #.
redactions: 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Every maximal digit run has exactly one transition from non-digit to digit, so it produces exactly one marker and count. Every non-digit is printed once unchanged.

## Complexity

O(L) time and O(L) storage.

## Common pitfalls

Do not emit one marker per digit, exclude the input newline from the transformed content, and still print a newline for EOF-terminated input. Verify boundary inputs as well as the worked example.
