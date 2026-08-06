# Digit-Run Redactor

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A log line is sanitised by replacing each maximal consecutive run of ASCII digits with a single `#`, while retaining every other character.

## Requirements

Write a complete C program in `c1511_core_036.c`.

**Input:** Read one line of at most 1000 characters, possibly ending at end-of-file instead of newline.

**Output:** Print the redacted line and then `redactions: k`, the number of digit runs replaced.

**Assumptions:** Only characters `0` through `9` count as digits.

**Restrictions:** Store the line in a char array and scan it once. Do not call a regular-expression engine or external program.

Submit exactly the file `c1511_core_036.c`.

## Examples

Input:

```text
Room 12, shelf 003.
```

Output:

```text
Room #, shelf #.
redactions: 2
```

The two maximal digit runs are each replaced by one marker.

## Implementation notes

A digit begins a new run when the previous processed character was not a digit. Match every required label, space, punctuation mark, and newline exactly.

