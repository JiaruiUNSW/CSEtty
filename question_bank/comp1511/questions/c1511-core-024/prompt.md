# Trim and Collapse Spacing

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A command label may contain runs of spaces and tabs. It must be normalised to single spaces, with no whitespace at either end.

## Requirements

Write or repair the complete C program in `c1511_core_024.c`.

**Input:** Read one line up to newline or end-of-file. Horizontal whitespace means space or tab.

**Output:** Print the normalised text followed by exactly one newline.

**Assumptions:** All other characters, including punctuation, must be copied unchanged.

**Restrictions:** Use `getchar` and process the stream without storing the entire line.

Submit exactly the file `c1511_core_024.c`.

## Examples

Input:

```text
  hello   world 
```

Output:

```text
hello world
```

Leading and trailing spaces disappear, and the internal run becomes one space.

## Implementation notes

Remember pending whitespace only after some output exists, and emit it only when the next non-whitespace character arrives. Output spelling, spaces, punctuation, and newlines must match exactly.

