# Orbital Sample Inventory

## Background

An operator maintains orbital sample containers through a line-oriented command console. Entries appear dynamically and must remain correct across updates and removals.

## Requirements

Process commands until `END`: `ADD name delta`, `SET name value`, `REMOVE name`, `QUERY name`, and `TOTAL`. Missing names have value zero. `QUERY` prints `name value`; `TOTAL` prints `TOTAL sum`. Other commands print nothing.

**Exact rule.** The table maps unique names to signed values: `ADD` accumulates, `SET` replaces, `REMOVE` deletes, a missing `QUERY` returns zero, and `TOTAL` sums current values.

Submit `c1511_system_006.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
ADD alpha 5
ADD beta -2
SET beta 8
TOTAL
END
```

Output:

```text
TOTAL 13
```

## Implementation notes

Use a dynamic array of structs with bounded names. Growth must preserve existing records. Free the final allocation on every normal exit.
