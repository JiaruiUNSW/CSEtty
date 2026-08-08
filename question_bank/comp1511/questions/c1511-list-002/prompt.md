# Alternating Buoy Chain

## Background

A linked chain stores readings in arrival order. The caller owns the nodes; your metric must inspect them without losing the head or leaking memory in the supplied harness.

## Requirements

Complete `solve`. The harness converts every command-line argument to one list node, calls your function, prints `result: X`, and frees the chain. With no arguments the list is empty.

**Exact rule.** Compute `node[0] - node[1] + node[2] - ...` in list order.

Submit `c1511_list_002.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `3 -1 -1 4 0 -2`

Input:

```text
(empty)
```

Output:

```text
result: 1
```

## Implementation notes

Do not change the harness or print inside `solve`. Preserve every `next` link. Recursive variants should give the empty-list base case before accessing a node.
