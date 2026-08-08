# Same-Day Elapsed Minutes

## Background

Two 24-hour clock times describe the start and finish of an activity on the same day.

## Requirements

Write or repair the complete C program in `c1511_core_023.c`.

**Input:** One line contains start_hour, start_minute, end_hour, end_minute. The finish is not earlier than the start.

**Output:** Print `elapsed: k minutes`.

**Assumptions:** Hours are 0 through 23 and minutes are 0 through 59.

**Restrictions:** Define a `struct time` and a helper that converts a time to minutes after midnight.

Submit exactly the file `c1511_core_023.c`.

## Examples

Input:

```text
9 45 11 10
```

Output:

```text
elapsed: 85 minutes
```

From 09:45 to 11:10 is one hour and twenty-five minutes.

## Implementation notes

Convert both endpoints to the same unit before subtracting. Output spelling, spaces, punctuation, and newlines must match exactly.
