# Race Split Awards

This is an original C programming task for the local CSEExamTTY simulator.

## Background

Each runner has three integer split times. One award goes to the fastest total, and another to the most consistent runner with the smallest difference between largest and smallest split. Either tie goes to the lower bib number.

## Requirements

Write a complete C program in `c1511_core_035.c`.

**Input:** The first line contains n (1 <= n <= 100). Each following line contains unique bib, split1, split2, split3 as positive integers.

**Output:** Print `fastest: bib total` and `consistent: bib range`.

**Assumptions:** All totals fit in a C `int`.

**Restrictions:** Use an array of runner structs and separate helper functions for total and range.

Submit exactly the file `c1511_core_035.c`.

## Examples

Input:

```text
3
12 10 11 12
5 12 10 10
8 9 15 9
```

Output:

```text
fastest: 5 32
consistent: 5 2
```

Bib 5 has the smallest total; bibs 5 and 12 tie on range, so lower bib 5 wins consistency.

## Implementation notes

The two awards have independent comparisons and may select different runners. Match every required label, space, punctuation mark, and newline exactly.

