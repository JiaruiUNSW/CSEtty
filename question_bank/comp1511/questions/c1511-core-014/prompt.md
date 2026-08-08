# Descending Number Fence

## Background

A display uses a descending sequence of positive labels separated by fence symbols.

## Requirements

Write or repair the complete C program in `c1511_core_014.c`.

**Input:** One line contains n (1 <= n <= 20).

**Output:** Print n down to 1 on one line, placing `>` between adjacent values and no separator after 1.

**Assumptions:** n is always in range.

**Restrictions:** Use a loop; do not write separate print statements for individual values.

Submit exactly the file `c1511_core_014.c`.

## Examples

Input:

```text
4
```

Output:

```text
4>3>2>1
```

The labels descend by one and the three separators appear only between labels.

## Implementation notes

Print the separator based on whether another number follows. Output spelling, spaces, punctuation, and newlines must match exactly.
