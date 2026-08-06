# Race Split Awards — solution

## Approach

Initialise both winners from the first runner. Scan later runners, updating fastest by total then bib and consistent by range then bib.

## Correctness

Each maintained winner is the optimum of the processed prefix under its award's ordered keys. Separate induction for both comparisons proves the final winners are correct.

## Complexity

O(n) time and O(n) storage.

## Common pitfalls

Do not use average instead of total, compute range as max minus min, and apply bib ties independently for each award. Verify boundary inputs as well as the worked example.

