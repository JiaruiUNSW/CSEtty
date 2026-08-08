# All-Zero Sensor Rows — worked solution

## Idea in one sentence

Visit exactly the cells participating in all-zero sensor rows and maintain one scalar result.

## Exact rule

Count rows for which every cell is zero.

## Approach

Visit exactly the cells participating in all-zero sensor rows and maintain one scalar result. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Validate dimensions and read `rows * columns` values.
2. Choose loop bounds that match the cells or windows in the definition.
3. Update the result with each eligible cell exactly once.
4. Return the neutral value for an empty or too-small grid and print once.

## Worked example

Command arguments: `(no command-line arguments)`

Input:

```text
2 3
1 2 3
4 5 6
```

Output:

```text
result: 0
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

The nested loops enumerate every and only eligible grid position. Each update equals that position's contribution, so aggregation over all iterations yields the defined grid metric.

## Complexity

The algorithm uses `O(rows * columns)` time and stores at most 64 integers.

## Common pitfalls

Do not assume a square grid, use `rows` as the row stride, or access neighbours/windows before proving they exist.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
