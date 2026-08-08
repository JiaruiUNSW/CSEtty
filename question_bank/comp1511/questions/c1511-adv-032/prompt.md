# Recursive even-prefix filter

## Background

`struct node *keep_even_prefixes(struct node *head, int *running_sum)` retains a node exactly when the inclusive sum from the original head through that node is even.

## Requirements

- The supplied `main` initializes `*running_sum` to zero; update it for every original node, including removed nodes.
- Preserve retained-node order, free rejected nodes, and allocate nothing.
- Use recursion for progression through the list and return the new head.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

Command:

```text
./c1511_adv_032 1 1 2 3 1
```

Output:

```text
1 2 1
```

## Implementation notes

Decide whether the current node is kept immediately after adding its value, before the recursive call changes the running sum further. Submit `c1511_adv_032.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source.
