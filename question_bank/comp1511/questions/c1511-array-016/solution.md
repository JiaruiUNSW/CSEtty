# Distinct Specimen Labels — worked solution

## Idea in one sentence

Scan the array while maintaining exactly the state needed for distinct specimen labels.

## Exact rule

Count distinct integer values; repeated occurrences contribute only once.

## Approach

Scan the array while maintaining exactly the state needed for distinct specimen labels. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Read and validate `n`, then store exactly `n` values.
2. Initialise the metric's neutral state, including any previous-item state.
3. Visit every required index once (or every ordered pair for the pair-count task).
4. Print the final `long long` result with the required label.

## Worked example

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
result: 5
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

The helper examines precisely the indices named by the definition. Its maintained state equals the metric for the processed prefix; extending by one value adds exactly that value's contribution. Therefore the final state equals the metric for the complete array.

## Complexity

The scan uses `O(n)` time and `O(n)` input storage; the distinct/inversion variants intentionally use `O(n^2)` time. Auxiliary state is `O(1)`.

## Common pitfalls

Do not read neighbours at the endpoints, change the first/last tie rule, or treat zero as positive/negative unless stated. Handle `n == 0` before reading `values[0]`.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
