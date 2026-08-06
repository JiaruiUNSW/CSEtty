# Compass Quarter Turns

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A compass pointer is rotated by signed quarter turns. Positive turns are clockwise and negative turns are anticlockwise.

## Requirements

Write or repair the complete C program in `c1511_core_022.c`.

**Input:** One line contains an uppercase direction (`N`, `E`, `S`, or `W`) and turns (-100 <= turns <= 100).

**Output:** Print `direction: X` for the resulting direction.

**Assumptions:** The input direction is valid.

**Restrictions:** Represent directions with an enum and correctly normalise negative modulo results.

Submit exactly the file `c1511_core_022.c`.

## Examples

Input:

```text
S -1
```

Output:

```text
direction: E
```

One anticlockwise quarter turn from South points East.

## Implementation notes

Map N, E, S, W to consecutive values zero through three. Add turns, take modulo four, then repair a negative result. Output spelling, spaces, punctuation, and newlines must match exactly.

