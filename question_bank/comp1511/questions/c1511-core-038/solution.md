# Fleet Components — solution

## Approach

Scan every cell. On an unvisited occupied cell, increment the component count and run flood fill to mark and count its complete component, updating the largest size.

## Correctness

Flood fill reaches exactly the occupied cells connected to its start by orthogonal paths and marks each once. The outer scan starts one fill per distinct component, so both count and maximum size are exact.

## Complexity

O(rows * columns) time and O(rows * columns) grid plus worst-case recursion stack.

## Common pitfalls

Check bounds before indexing, mark before recursive calls, use only four directions, and report largest zero for an empty board. Verify boundary inputs as well as the worked example.

