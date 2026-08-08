# Triangle Label

## Background

Three positive integer lengths must first be checked as a triangle and then labelled by side equality.

## Requirements

Write or repair the complete C program in `c1511_core_027.c`.

**Input:** One line contains positive integers a, b, and c.

**Output:** Print `triangle: invalid` when any two sides sum to at most the third. Otherwise print `triangle: equilateral`, `triangle: isosceles`, or `triangle: scalene`.

**Assumptions:** Pairwise sums fit in a C `int`.

**Restrictions:** Use conditional statements. Validate the triangle before classifying equality.

Submit exactly the file `c1511_core_027.c`.

## Examples

Input:

```text
5 5 8
```

Output:

```text
triangle: isosceles
```

The lengths satisfy all triangle inequalities and exactly two sides are equal.

## Implementation notes

All three triangle inequalities are required because the sides are not supplied in sorted order. Output spelling, spaces, punctuation, and newlines must match exactly.
