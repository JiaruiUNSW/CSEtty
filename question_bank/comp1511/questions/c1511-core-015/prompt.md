# Signal State Advances

## Background

A three-state signal repeats the cycle Red, Green, Amber, Red. The input gives a starting state and a number of advances.

## Requirements

Write or repair the complete C program in `c1511_core_015.c`.

**Input:** One line contains a state character (`R`, `G`, or `A`) and steps (0 <= steps <= 100).

**Output:** Print `state: X` using the final state character.

**Assumptions:** The state character is uppercase and valid.

**Restrictions:** Define and use a C `enum` for the states. Advance through the cycle rather than encoding a table of all possible step counts.

Submit exactly the file `c1511_core_015.c`.

## Examples

Input:

```text
G 2
```

Output:

```text
state: R
```

Two advances from Green move through Amber to Red.

## Implementation notes

Reducing steps modulo three is optional; a small loop is sufficient. Output spelling, spaces, punctuation, and newlines must match exactly.
