# Triangle Support Code — worked solution

## Idea in one sentence

Compare the three values in a fixed order to compute triangle support code.

## Exact rule

Return 0 for invalid sides; otherwise return 3 for equilateral, 2 for isosceles, and 1 for scalene.

## Approach

Compare the three values in a fixed order to compute triangle support code. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Read all three values and identify any ordering-independent bounds.
2. Apply equality and validity rules before the general branches.
3. Resolve ties using the order stated in the task.
4. Print the resulting integer code.

## Worked example

Input:

```text
-4 9 2
```

Output:

```text
result: 0
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

The branch conditions partition all possible triples into the cases in the specification. Each branch returns the value defined for its case, so exactly one correct result is produced.

## Complexity

A constant number of comparisons uses `O(1)` time and `O(1)` space.

## Common pitfalls

Test equal values, negative values, and values exactly on a branch boundary. Avoid chained C comparisons such as `a < b < c`.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
