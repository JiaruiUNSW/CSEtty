# Museum Crate Journal — worked solution

## Idea in one sentence

Maintain one authoritative dynamic table and interpret each command as a small state transition.

## Exact rule

The table maps unique names to signed values: `ADD` accumulates, `SET` replaces, `REMOVE` deletes, a missing `QUERY` returns zero, and `TOTAL` sums current values.

## Approach

Maintain one authoritative dynamic table and interpret each command as a small state transition. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Read one command token and dispatch before reading command-specific fields.
2. Search for the named record and create it only for `ADD` or `SET`.
3. Apply the transition, growing the table safely when needed.
4. Print only query results, then free the table after `END`.

## Worked example

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

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

Initially the table represents the empty mapping. Each command branch performs exactly the mapping update or observation in its definition, preserving the representation invariant that names are unique. By induction, every query and total reflects all preceding commands.

## Complexity

With `m` commands and at most `n` names, linear search gives `O(mn)` time and the dynamic table uses `O(n)` space.

## Common pitfalls

Do not create entries for `QUERY`/`REMOVE`, lose the old pointer when `realloc` fails, print update acknowledgements, or forget that repeated `ADD` accumulates.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
