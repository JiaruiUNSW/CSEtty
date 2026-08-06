# Alphabet Histogram

This is an original C programming task for the local CSEExamTTY simulator.

## Background

A lowercase word is summarised as a sparse alphabet histogram, listing only letters that actually occur.

## Requirements

Write a complete C program in `c1511_core_033.c`.

**Input:** One lowercase word containing 1 through 100 characters.

**Output:** For each present letter in alphabetic order, print `letter: count`. Finally print `distinct: k`.

**Assumptions:** Every character is between `a` and `z`.

**Restrictions:** Use a 26-element integer array. Do not sort the input or write 26 separate counting branches.

Submit exactly the file `c1511_core_033.c`.

## Examples

Input:

```text
banana
```

Output:

```text
a: 3
b: 1
n: 2
distinct: 3
```

Only a, b, and n occur, and the lines are alphabetically ordered.

## Implementation notes

Character subtraction maps a lowercase letter to an array index. Count distinct letters when printing or when a frequency first changes from zero. Match every required label, space, punctuation mark, and newline exactly.

