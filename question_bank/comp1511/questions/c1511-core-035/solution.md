# Race Split Awards — solution

## Approach

Initialise both winners from the first runner. Scan later runners, updating fastest by total then bib and consistent by range then bib.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `same-winner`, runs `./c1511_core_035`.

Input:

```text
3
12 10 11 12
5 12 10 10
8 9 15 9
```

Expected standard output:

```text
fastest: 5 32
consistent: 5 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each maintained winner is the optimum of the processed prefix under its award's ordered keys. Separate induction for both comparisons proves the final winners are correct.

## Complexity

O(n) time and O(n) storage.

## Common pitfalls

Do not use average instead of total, compute range as max minus min, and apply bib ties independently for each award. Verify boundary inputs as well as the worked example.
