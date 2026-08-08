# Character Run Count — solution

## Approach

Initialise the count to one and scan from index one, incrementing whenever the current character differs from the previous character.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `three-runs`, runs `./c1511_core_025`.

Input:

```text
aaabbc
```

Expected standard output:

```text
runs: 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The first character starts the first run. Every remaining run starts at exactly a position where adjacent characters differ, so counting those boundaries plus one gives the exact number.

## Complexity

O(L) time and O(L) input storage.

## Common pitfalls

Do not count individual repeated characters as separate runs, and begin the scan at the second character. Keep the submitted filename and required output format unchanged.
