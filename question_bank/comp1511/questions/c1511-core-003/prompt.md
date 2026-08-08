# Cyclic Trail Distance

## Background

Checkpoints form a closed trail. The travel cost between consecutive checkpoints is the absolute difference between their integer labels, including the edge from the last checkpoint back to the first.

## Requirements

Write a complete C program in `c1511_core_003.c`.

**Input:** The first line contains n (2 <= n <= 100). The next line contains n integer checkpoint labels.

**Output:** Print `distance: s`, where s is the sum of all n cyclic edge costs.

**Assumptions:** The final sum fits in a C `int`.

**Restrictions:** Store labels in an array and compute the cyclic distance in a function. Do not duplicate the first item in the input.

Submit exactly the file `c1511_core_003.c`.

## Examples

Input:

```text
4
1 4 2 6
```

Output:

```text
distance: 14
```

The four costs are 3, 2, 4, and 5.

## Implementation notes

Modulo indexing can select the next checkpoint for the last element. A small integer absolute-value helper avoids changing the array. Your output must match the specified spelling, spacing, and newlines exactly.
