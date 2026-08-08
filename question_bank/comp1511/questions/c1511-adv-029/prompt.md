# Recursive mirror check

## Background

`int is_mirror_sequence(const struct node *head)` recursively decides whether list values read the same from both ends, without arrays or mutation.

## Requirements

- Return 1 for empty and one-node lists and 0 for a mismatch.
- Do not allocate memory, change links/data, or first copy values into an array.
- The executable prints `YES` for 1 and `NO` for 0.
- Produce exactly the demonstrated text on valid input and leave no heap allocation unreachable.

## Examples

Command:

```text
./c1511_adv_029 1 2 1
```

Output:

```text
YES
```

## Implementation notes

One recursive pointer can move to the end while a pointer-to-pointer advances from the front during unwinding. Submit `c1511_adv_029.c`. Modify only the marked function or helper region, retain the testable command-line interface, and submit the uniquely named source.
