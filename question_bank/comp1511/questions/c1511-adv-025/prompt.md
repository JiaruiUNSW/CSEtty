# Recursive neighbouring totals

## Background

`struct node *pair_totals(const struct node *head)` recursively builds a new list containing the sum of each adjacent input pair; an unpaired final value is copied unchanged.

## Requirements

- Leave the input list and all its links unchanged.
- Allocate one result node per pair, plus one for an odd final node, and preserve pair order.
- Return `NULL` for empty input; the supplied `main` separately frees both lists.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

Command:

```text
./c1511_adv_025 1 2 3 4 5
```

Output:

```text
3 7 5
```

## Implementation notes

The recursive call can advance by two nodes when a pair exists. Assume each pair sum fits in `int`. Submit `c1511_adv_025.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source.
