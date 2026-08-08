# Restock Manifest

## Background

A storeroom records an item identifier, current stock, and target stock for each product. Products below target must appear in a restock manifest in their original input order.

## Requirements

Write a complete C program in `c1511_core_029.c`.

**Input:** The first line contains n (1 <= n <= 100). Each of the next n lines contains id, current, and target as non-negative integers. IDs are unique.

**Output:** For each item with current less than target, print `id: need`, where need is target minus current. Finally print `total needed: t`. Items at or above target produce no item line.

**Assumptions:** All differences and their total fit in a C `int`.

**Restrictions:** Store records in an array of `struct item` and use a helper to calculate one item's needed quantity. Do not reorder records.

Submit exactly the file `c1511_core_029.c`.

## Examples

Input:

```text
3
101 5 8
102 10 7
103 0 2
```

Output:

```text
101: 3
103: 2
total needed: 5
```

Items 101 and 103 are short by three and two units; item 102 already exceeds target.

## Implementation notes

A helper may return zero for any item that does not require stock. Preserve input order when printing. Match every required label, space, punctuation mark, and newline exactly.
