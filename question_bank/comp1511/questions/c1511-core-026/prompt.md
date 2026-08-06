# Repair the Clock Wrap

This is an original C programming task for the local CSEExamTTY simulator.

## Background

The supplied clock program adds a signed minute offset, but it wraps by the wrong unit and mishandles negative remainders.

## Requirements

Write or repair the complete C program in `c1511_core_026.c`.

**Input:** One line contains hour, minute, and offset. The time is valid and -1440 <= offset <= 1440.

**Output:** Print the resulting 24-hour time as exactly `HH:MM` with leading zeroes.

**Assumptions:** Adding the offset may cross midnight in either direction.

**Restrictions:** Repair the arithmetic in the supplied program while retaining its input and output interface.

Submit exactly the file `c1511_core_026.c`.

## Examples

Input:

```text
23 50 20
```

Output:

```text
00:10
```

Twenty minutes after 23:50 is ten minutes after midnight.

## Implementation notes

A day contains 1440 minutes. After remainder, add 1440 if the total is negative before splitting into hours and minutes. Output spelling, spaces, punctuation, and newlines must match exactly.

