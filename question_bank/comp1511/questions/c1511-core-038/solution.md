# Fleet Components — solution

## Approach

Scan every cell. On an unvisited occupied cell, increment the component count and run flood fill to mark and count its complete component, updating the largest size.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `two-components`, runs `./c1511_core_038`.

Input:

```text
3 5
##...
.#..#
....#
```

Expected standard output:

```text
components: 2
largest: 3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Flood fill reaches exactly the occupied cells connected to its start by orthogonal paths and marks each once. The outer scan starts one fill per distinct component, so both count and maximum size are exact.

## Complexity

O(rows * columns) time and O(rows * columns) grid plus worst-case recursion stack.

## Common pitfalls

Check bounds before indexing, mark before recursive calls, use only four directions, and report largest zero for an empty board. Verify boundary inputs as well as the worked example.
