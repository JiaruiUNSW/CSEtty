# Alternating-position total

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int alternating_position_total(const struct node *head)` returns the sum of values at zero-based positions 0, 2, 4, and so on.

## Requirements

- Traverse the list once without changing any node or link.
- An empty list returns `0`; position zero is included.
- Use the supplied `main`, list builder, printer-freeing helpers, and change only the marked function.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_001 4 7 1 9
```

Output:

```text
5
```

## Implementation notes

Assume the mathematical result fits in an `int`. Do not allocate memory, use arrays, or count the list in a separate pass. Submit `c1511_adv_001.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
