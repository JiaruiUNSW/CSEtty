# Parenthesis Stream Audit

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A line of text may contain nested parentheses mixed with arbitrary other characters. The audit records whether parentheses are balanced and the greatest nesting depth reached.

## Requirements

Write or repair the complete C program in `c1511_core_017.c`.

**Input:** Read characters from standard input until newline or end-of-file.

**Output:** Print `valid: yes` or `valid: no`, then print `max depth: k`. A closing parenthesis without an available opener makes the line invalid; unmatched openers at the end also make it invalid.

**Assumptions:** The line contains at most 1000 characters.

**Restrictions:** Process the stream with `getchar`. Do not store the complete line or use a stack array.

Submit exactly the file `c1511_core_017.c`.

## Examples

Input:

```text
(a(b)c)
```

Output:

```text
valid: yes
max depth: 2
```

The inner pair reaches depth two and every opener is closed.

## Implementation notes

Track current depth, maximum depth, and an invalid flag. Do not let an unmatched closing parenthesis make the depth negative. Output spelling, spaces, punctuation, and newlines must match exactly.

