# Temperature Drift

## Background

A weather station compares an initial integer temperature with a later reading.

## Requirements

Write or repair the complete C program in `c1511_core_020.c`.

**Input:** One line contains start and end temperatures.

**Output:** Print `change: d`, where d is end minus start. Then print `direction: rising`, `direction: falling`, or `direction: steady`.

**Assumptions:** The subtraction fits in a C `int`.

**Restrictions:** Use integer arithmetic and conditional statements.

Submit exactly the file `c1511_core_020.c`.

## Examples

Input:

```text
12 17
```

Output:

```text
change: 5
direction: rising
```

The later reading is five degrees higher.

## Implementation notes

Classify the sign of the computed change rather than repeating the subtraction in every branch. Output spelling, spaces, punctuation, and newlines must match exactly.
