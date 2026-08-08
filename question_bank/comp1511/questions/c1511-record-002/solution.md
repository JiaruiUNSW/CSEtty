# Positive Wildlife Records — worked solution

## Idea in one sentence

Store each input row as one struct and compute positive wildlife records over the resulting record array.

## Exact rule

Count records whose value is strictly greater than zero.

## Approach

Store each input row as one struct and compute positive wildlife records over the resulting record array. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Read and validate the record count.
2. Populate one complete struct per input row.
3. Apply the metric without separating names from their values.
4. Print the final scalar using the stated tie rule.

## Worked example

Command arguments: `(no command-line arguments)`

Input:

```text
4
a 3
b -1
c 3
d 8
```

Output:

```text
result: 3
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

Every input row becomes exactly one array element in the same order. The helper's scan/pair enumeration matches the metric definition, so the final scalar is correct for all records.

## Complexity

Most variants run in `O(n)` time; the equal-pair variant uses `O(n^2)`. The record array uses `O(n)` space.

## Common pitfalls

Limit `%s`, handle `n == 0`, and keep first-versus-last tie behaviour explicit.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
