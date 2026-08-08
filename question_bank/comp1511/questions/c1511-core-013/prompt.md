# Metro Fare Band

## Background

A tiny ticket machine calculates an integer fare from journey distance and whether the trip occurs during a peak period.

## Requirements

Write or repair the complete C program in `c1511_core_013.c`.

**Input:** One line contains distance and peak. Distance is an integer from 0 to 100 kilometres; peak is 0 or 1.

**Output:** Start with fare 4. Add 0 for distance at most 5, add 3 for distance 6 through 15, or add 7 for distance above 15. Finally add 2 when peak is 1. Print `fare: $k`.

**Assumptions:** The supplied distance and peak flag are always valid.

**Restrictions:** Use conditional statements and integer arithmetic. Do not use arrays or loops.

Submit exactly the file `c1511_core_013.c`.

## Examples

Input:

```text
10 1
```

Output:

```text
fare: $9
```

The base 4 plus the middle-distance surcharge 3 plus peak surcharge 2 gives 9.

## Implementation notes

Choose exactly one distance surcharge, then independently apply the peak surcharge. Output spelling, spaces, punctuation, and newlines must match exactly.
