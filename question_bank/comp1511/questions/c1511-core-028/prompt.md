# Weighted Letter Checksum

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A line receives a checksum from its ASCII letters. Ignoring case and non-letters, the first accepted letter is weighted by 1, the second by 2, and so on; letter values are A=1 through Z=26.

## Requirements

Write or repair the complete C program in `c1511_core_028.c`.

**Input:** Read characters up to newline or end-of-file.

**Output:** Print `checksum: s`.

**Assumptions:** The line has at most 1000 characters and the checksum fits in a C `int`.

**Restrictions:** Use `getchar`, do not store the complete line, and do not call external programs.

Submit exactly the file `c1511_core_028.c`.

## Examples

Input:

```text
A-bC!
```

Output:

```text
checksum: 14
```

The accepted letters A, b, C contribute 1*1 + 2*2 + 3*3.

## Implementation notes

Write a helper returning zero for non-letters and 1 through 26 for either case of a letter. Output spelling, spaces, punctuation, and newlines must match exactly.

