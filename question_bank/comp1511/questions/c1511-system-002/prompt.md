# Rescue Supply Register

## Task

The table maps unique names to signed values: `ADD` accumulates, `SET` replaces, `REMOVE` deletes, a missing `QUERY` returns zero, and `TOTAL` sums current values.

## Background

An operator maintains rescue supply bins through a line-oriented command console. Entries appear dynamically and must remain correct across updates and removals.

## Requirements

Process commands until `END`: `ADD name delta`, `SET name value`, `REMOVE name`, `QUERY name`, and `TOTAL`. Missing names have value zero. `QUERY` prints `name value`; `TOTAL` prints `TOTAL sum`. Other commands print nothing.

## Starter code

Complete the marked command loop and dynamic record table in `main`. This is a whole-program task; the starter provides only the data definition and includes.

## Examples

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

## Submission

Submit `c1511_system_002.c` only. Your program must not print prompts, labels, or explanatory text unless the required output format explicitly includes them.
