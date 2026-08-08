# First prefix threshold

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `int first_prefix_at_least(const struct node *head, int target)` returns the first zero-based index whose inclusive prefix sum is at least `target`, or `-1` if none exists.

## Requirements

- The first argument to the executable is the target; remaining arguments form the list.
- Test the prefix after adding each current node.
- Do not alter the nodes and do not assume values are positive.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_003 6 2 1 3
```

Output:

```text
2
```

## Implementation notes

The supplied `main` requires a target and reports usage with exit status 2 otherwise. Assume every prefix sum fits in `long`. Submit `c1511_adv_003.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
