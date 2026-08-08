# Most Improved Student

## Background

A class stores student IDs with before and after scores. The most improved student has the largest after-minus-before gain; ties prefer the higher after score, then the lower ID.

## Requirements

Write a complete C program in `c1511_core_032.c`.

**Input:** The first line contains n (1 <= n <= 100). Each following line contains unique id, before, and after scores.

**Output:** Print `student: id` and `gain: g` for the selected record.

**Assumptions:** Scores are integers from 0 through 100.

**Restrictions:** Use an array of structs and a helper that decides whether one record ranks ahead of another.

Submit exactly the file `c1511_core_032.c`.

## Examples

Input:

```text
3
42 60 75
17 70 85
99 50 64
```

Output:

```text
student: 17
gain: 15
```

Students 42 and 17 both gain 15, but 17 has the higher after score.

## Implementation notes

A gain may be negative. Initialise the winner from the first record rather than assuming gains are non-negative. Match every required label, space, punctuation mark, and newline exactly.
