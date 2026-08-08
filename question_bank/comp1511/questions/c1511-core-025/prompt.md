# Character Run Count

## Background

A run is a maximal consecutive block of the same character in a word. The task counts how many runs form the word.

## Requirements

Write or repair the complete C program in `c1511_core_025.c`.

**Input:** One non-empty word of at most 100 characters with no whitespace.

**Output:** Print `runs: k`.

**Assumptions:** Comparison is case-sensitive.

**Restrictions:** Store the input as a null-terminated string and scan it once without modifying it.

Submit exactly the file `c1511_core_025.c`.

## Examples

Input:

```text
aaabbc
```

Output:

```text
runs: 3
```

The maximal blocks are `aaa`, `bb`, and `c`.

## Implementation notes

A non-empty word begins with one run. Each later character different from its predecessor begins one additional run. Output spelling, spaces, punctuation, and newlines must match exactly.
