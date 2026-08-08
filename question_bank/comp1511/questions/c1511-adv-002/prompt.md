# Record-high counter

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int count_record_highs(const struct node *head)` counts nodes whose value is strictly greater than every earlier value. The first node, when present, is a record.

## Requirements

- Visit nodes from left to right and do not mutate the list.
- Equal values do not establish a new record.
- Return `0` for an empty list and use no arrays or allocation inside the function.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_002 3 1 4 4 7
```

Output:

```text
3
```

## Implementation notes

Values may be negative. Modify only the marked function in the starter program. Submit `c1511_adv_002.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
