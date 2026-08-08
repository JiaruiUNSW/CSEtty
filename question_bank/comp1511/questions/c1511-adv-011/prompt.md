# Outside-in weave

## Background

The supplied `main` converts each listed integer into one heap-allocated node so that the target function can be tested without any external files. `struct node *outside_in(struct node *head)` reorders `a0,a1,...,an` into `a0,an,a1,a(n-1),...` by relinking existing nodes.

## Requirements

- Allocate and free no nodes and change no data.
- Handle odd and even lengths, preserving the single middle node for odd lengths.
- Return a properly terminated acyclic list.
- The program must print exactly the value or list format demonstrated below and write no diagnostic text on success.

## Examples

Command:

```text
./c1511_adv_011 1 2 3 4 5
```

Output:

```text
1 5 2 4 3
```

## Implementation notes

A useful decomposition is split, reverse the second half, then weave. Submit `c1511_adv_011.c`. The supplied `main` validates ownership by freeing all surviving nodes, so do not retain hidden aliases.
