# Line Initials

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A short title contains words separated by one or more spaces or tabs. Its initials are the uppercase form of the first character of each word.

## Requirements

Write a complete C program in `c1511_core_030.c`.

**Input:** Read one line of at most 200 characters. Every non-empty word starts with an ASCII letter; separators are spaces or tabs.

**Output:** Print `initials: X` followed by `words: k`. A line containing only separators has empty initials and zero words.

**Assumptions:** Other non-separator characters inside a word are copied only indirectly through its initial; input may end without a newline.

**Restrictions:** Store the line in a char array, scan it once, and write a helper that converts one lowercase ASCII letter to uppercase.

Submit exactly the file `c1511_core_030.c`.

## Examples

Input:

```text
hello   wide world
```

Output:

```text
initials: HWW
words: 3
```

The three words begin with h, w, and w.

## Implementation notes

A character begins a word when it is not a separator and either has index zero or follows a separator. Match every required label, space, punctuation mark, and newline exactly.

