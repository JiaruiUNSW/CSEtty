# Vowel Bookends

## Background

A lowercase word is summarised by its vowel count and whether vowels appear at both ends.

## Requirements

Write or repair the complete C program in `c1511_core_018.c`.

**Input:** One lowercase word of length 1 through 100, containing only `a` through `z`.

**Output:** Print `vowels: k` and then `bookended: yes` when both the first and last characters are vowels, otherwise `bookended: no`.

**Assumptions:** The input has no spaces and fits in the supplied array.

**Restrictions:** Use a null-terminated C string and write a helper that decides whether one character is a vowel.

Submit exactly the file `c1511_core_018.c`.

## Examples

Input:

```text
apple
```

Output:

```text
vowels: 2
bookended: yes
```

The word contains `a` and `e`, and both endpoints are vowels.

## Implementation notes

Find the string length while counting, or use the standard string length function after input. Output spelling, spaces, punctuation, and newlines must match exactly.
