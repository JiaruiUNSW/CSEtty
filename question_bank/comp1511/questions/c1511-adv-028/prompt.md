# Recursive reverse copy

## Background

`struct node *reverse_copy(const struct node *head)` recursively returns a deep copy whose order is the reverse of the input.

## Requirements

- Do not modify, relink, or free any input node.
- Allocate exactly one new node for each input node and copy every integer.
- Return `NULL` for empty input; the supplied `main` frees input and result independently.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

Command:

```text
./c1511_adv_028 1 2 3
```

Output:

```text
3 2 1
```

## Implementation notes

A recursive helper can carry the partially built reversed copy as an accumulator. Submit `c1511_adv_028.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source.
