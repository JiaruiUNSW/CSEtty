# Longest rising-or-level run

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int longest_nondecreasing_run(const struct node *head)` returns the length of the longest contiguous run in which each value is at least its predecessor.

## Requirements

- Treat runs as contiguous portions of the list, not subsequences.
- A one-node list has result `1`; an empty list has result `0`.
- Do not modify links or data and traverse at most once.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_004 3 3 5 2 4
```

Output:

```text
3
```

## Implementation notes

Keep both the current run length and best length. Modify only the marked function. Submit `c1511_adv_004.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
