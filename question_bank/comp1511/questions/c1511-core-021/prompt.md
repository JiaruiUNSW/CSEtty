# Alternating Digit Score

## Background

A serial number receives a score by reading digits from right to left: add the first digit, subtract the next, then alternate.

## Requirements

Write or repair the complete C program in `c1511_core_021.c`.

**Input:** One line contains a non-negative integer value from 0 through 1000000000.

**Output:** Print `score: s`.

**Assumptions:** The final score fits in a C `int`.

**Restrictions:** Use arithmetic digit extraction with division and remainder. Do not convert the number to a string.

Submit exactly the file `c1511_core_021.c`.

## Examples

Input:

```text
12345
```

Output:

```text
score: 3
```

From the right, the calculation is 5 - 4 + 3 - 2 + 1.

## Implementation notes

A do-while loop naturally processes the input value zero as one zero digit. Output spelling, spaces, punctuation, and newlines must match exactly.
